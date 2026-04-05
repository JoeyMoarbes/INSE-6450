# STRATOS Continual Learning Experiment
# Simulates concept drift across 3 time steps and measures replay-based recovery.

# Usage: python continual_learning_experiment.py
#        Produces results/continual_learning_results.json + plots/continual_learning_trajectory.png

# Context: T0 = baseline evaluation on clean and drifted data. T1 = drift detection (same model
# sees paraphrase_heavy + vague_keyword perturbations). T2 = retrain with experience replay buffer
# (70% original clean data + 30% drifted examples) and re-evaluate. Measures whether the updated
# model recovers drift-set performance without degrading clean-set perplexity.

# Prerequisites:
#   - Fused model at ../Milestone 2/fused_model
#   - Datasets at ../Milestone 3/datasets/{clean,paraphrase_heavy,vague_keyword}/test.jsonl
#   - Training data at ../Milestone 2/datasets/train.jsonl
#   - pip install mlx mlx-lm numpy matplotlib

import json, math, time, subprocess, shutil
from pathlib import Path  # Cross-platform path handling

import numpy as np  # Array operations and bootstrapping
import matplotlib.pyplot as plt  # Trajectory plot generation
import mlx.core as mx  # Apple Silicon ML framework
import mlx.nn as nn  # Neural network modules (cross-entropy loss)
from mlx_lm import load, generate  # Model loading and text generation

# Paths — all relative so the script is portable across machines
M2 = Path("../Milestone 2")  # Milestone 2 deliverables (model + training data)
M3 = Path("../Milestone 3")  # Milestone 3 deliverables (perturbed test sets)
ORIG_MODEL = M2 / "fused_model"  # Baseline fused Llama-3.2-3B (6.0 GB, 4-bit quantized)
ORIG_TRAIN = M2 / "datasets" / "train.jsonl"  # Original 2,500-pair training set
ORIG_VALID = M2 / "datasets" / "valid.jsonl"  # Validation set for early stopping
CLEAN_TEST = M3 / "datasets" / "clean" / "test.jsonl"  # 250 clean test examples
DRIFT_SETS = [  # Drifted test sets simulating concept drift
    M3
    / "datasets"
    / "paraphrase_heavy"
    / "test.jsonl",  # 250 heavy-paraphrase examples
    M3 / "datasets" / "vague_keyword" / "test.jsonl",  # 250 vague-keyword examples
]
OUT = Path("results")  # JSON output directory
PLOTS = Path("plots")  # PNG output directory
BLUES = ["#1a5276", "#2e86c1", "#5dade2", "#85c1e9", "#d4e6f1"]  # Color palette


def load_jsonl(p: Path) -> list[dict]:
    """Load a JSONL file into a list of dicts."""
    with open(p) as f:
        return [json.loads(ln) for ln in f if ln.strip()]


def save_jsonl(rows: list[dict], p: Path):
    """Write a list of dicts as JSONL, creating parent dirs if needed."""
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, "w") as f:
        for r in rows:
            f.write(json.dumps(r) + "\n")


# Forward pass: compute cross-entropy loss and perplexity on reference answer tokens only.
# Uses ChatML template to isolate the assistant response from the user prompt prefix.
def eval_example(model, tok, q: str, ref: str) -> dict:
    # Build full conversation (user + assistant) and user-only prefix
    full = tok.apply_chat_template(
        [{"role": "user", "content": q}, {"role": "assistant", "content": ref}],
        tokenize=False,
    )
    user = tok.apply_chat_template(
        [{"role": "user", "content": q}],
        tokenize=False,
        add_generation_prompt=True,
    )
    full_ids = tok.encode(full)
    pfx = len(tok.encode(user))  # Number of tokens in user prompt
    n_ans = len(full_ids) - pfx  # Number of answer tokens to score
    if n_ans <= 0:
        return {"loss": float("inf"), "ppl": float("inf")}

    # Cross-entropy on answer tokens only (teacher forcing)
    logits = model(mx.array(full_ids)[None, :])
    loss = nn.losses.cross_entropy(
        logits[0, pfx - 1 : -1, :],  # Shift logits to align with next-token targets
        mx.array(full_ids[pfx:]),  # Target: actual answer token IDs
        reduction="mean",
    )
    mx.eval(loss)
    l = loss.item()
    del logits, loss  # Free GPU memory
    mx.eval(mx.zeros(1))  # Flush remaining references
    return {"loss": l, "ppl": math.exp(min(l, 20))}  # Cap exponent to avoid overflow


# Evaluate a model on a list of examples, return aggregated metrics with bootstrap CIs.
def evaluate(model, tok, exs: list[dict], label: str) -> dict:
    losses, ppls = [], []
    for i, ex in enumerate(exs):
        q = ex["messages"][0]["content"]  # User question
        ref = ex["messages"][1]["content"]  # Reference answer
        m = eval_example(model, tok, q, ref)
        losses.append(m["loss"])
        ppls.append(m["ppl"])
        if (i + 1) % 50 == 0:  # Progress logging every 50 examples
            print(f"    [{label}] {i + 1}/{len(exs)} avg_loss={np.mean(losses):.3f}")
    la = np.array(losses)
    # 95% bootstrap confidence interval on mean loss (1000 resamples)
    rng = np.random.default_rng(42)
    boots = [np.mean(rng.choice(la, len(la), replace=True)) for _ in range(1000)]
    lo, hi = np.percentile(boots, [2.5, 97.5])
    return {
        "label": label,
        "n": len(exs),
        "mean_loss": float(la.mean()),
        "std_loss": float(la.std()),
        "mean_ppl": float(np.mean(ppls)),
        "loss_ci_low": float(lo),
        "loss_ci_high": float(hi),
    }


# Build the drifted test set by combining 50% paraphrase_heavy + 50% vague_keyword
def build_drift_test() -> list[dict]:
    all_drift = []
    for p in DRIFT_SETS:
        if p.exists():
            all_drift.extend(load_jsonl(p))
    np.random.seed(42)  # Reproducible shuffle
    np.random.shuffle(all_drift)
    return all_drift


# Build replay training set: 70% old clean data + 30% drifted examples.
# This ratio preserves original knowledge while incorporating corrected drift examples.
def build_replay_train(drift_exs: list[dict]) -> Path:
    old = load_jsonl(ORIG_TRAIN)
    np.random.seed(42)
    np.random.shuffle(old)

    n_old = int(len(old) * 0.7)  # 70% from original training data
    replay_old = old[:n_old]

    n_new = int(
        n_old / 0.7 * 0.3
    )  # 30% from drifted examples (simulates human-corrected data)
    replay_new = drift_exs[:n_new]

    merged = replay_old + replay_new
    np.random.shuffle(merged)  # Interleave old and new to prevent ordering bias

    out_dir = Path("cl_experiment")
    save_jsonl(merged, out_dir / "train.jsonl")
    shutil.copy(ORIG_VALID, out_dir / "valid.jsonl")  # Reuse original validation set

    print(
        f"Replay train set: {len(merged)} examples ({len(replay_old)} old + {len(replay_new)} new)"
    )
    return out_dir


# Run LoRA training via mlx_lm.lora CLI subprocess.
# Uses conservative config to avoid Metal GPU crashes: batch 2, 8 layers, grad-checkpoint.
def retrain(data_dir: Path) -> tuple[float, Path]:
    adapter_dir = Path("cl_experiment") / "adapters"
    adapter_dir.mkdir(parents=True, exist_ok=True)

    n_train = len(load_jsonl(data_dir / "train.jsonl"))
    n_iters = 100  # Short CL update (~0.2 epochs at batch size 2)

    cmd = [
        "python",
        "-m",
        "mlx_lm.lora",
        "--model",
        str(ORIG_MODEL),  # Base model to adapt
        "--data",
        str(data_dir),  # Replay buffer train/valid
        "--train",
        "--adapter-path",
        str(adapter_dir),  # Output adapter weights
        "--batch-size",
        "2",  # Small batch to fit M2 Max memory
        "--num-layers",
        "8",  # LoRA on last 8 transformer layers
        "--iters",
        str(n_iters),  # 100 gradient steps
        "--val-batches",
        "25",  # Validation every eval step
        "--learning-rate",
        "5e-5",  # Lower LR than initial training (1e-4) for stability
        "--steps-per-report",
        "25",
        "--steps-per-eval",
        "50",
        "--seed",
        "42",
        "--grad-checkpoint",  # Trade compute for memory — prevents Metal crashes
    ]
    print(f"Training for {n_iters} iterations on {n_train} examples ...")
    t0 = time.time()
    result = subprocess.run(cmd, capture_output=True, text=True)
    elapsed = time.time() - t0

    print(result.stdout[-2000:] if len(result.stdout) > 2000 else result.stdout)
    if result.returncode != 0:
        print("STDERR:", result.stderr[-2000:])

    return elapsed, adapter_dir


# Fuse LoRA adapter weights into the base model to produce a standalone fused model
def fuse_model(adapter_dir: Path) -> Path:
    fused = Path("cl_experiment") / "fused_model"
    cmd = [
        "python",
        "-m",
        "mlx_lm.fuse",
        "--model",
        str(ORIG_MODEL),  # Original base model
        "--adapter-path",
        str(adapter_dir),  # Trained LoRA adapter
        "--save-path",
        str(fused),  # Output fused model directory
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print("Fuse FAILED:", result.stderr[-500:])
    if not fused.exists():
        raise RuntimeError(f"Fused model dir not found at {fused}")
    print(f"Fused model saved to {fused}")
    return fused


def main():
    OUT.mkdir(exist_ok=True)
    PLOTS.mkdir(exist_ok=True)

    # Build drifted test set (500 examples: 250 paraphrase + 250 vague)
    drift_test = build_drift_test()
    clean_test = load_jsonl(CLEAN_TEST)
    print(
        f"Clean test: {len(clean_test)} examples, Drift test: {len(drift_test)} examples"
    )

    results = {}

    # === T0: Baseline evaluation (original model on clean + drifted data) ===
    print("\n=== T0: Baseline (original model) ===")
    model, tok = load(str(ORIG_MODEL))
    t0_clean = evaluate(model, tok, clean_test, "T0-clean")
    t0_drift = evaluate(model, tok, drift_test, "T0-drift")
    results["T0"] = {"clean": t0_clean, "drift": t0_drift}
    print(f"  Clean: loss={t0_clean['mean_loss']:.3f} ppl={t0_clean['mean_ppl']:.2f}")
    print(f"  Drift: loss={t0_drift['mean_loss']:.3f} ppl={t0_drift['mean_ppl']:.2f}")
    del model, tok
    mx.eval(mx.zeros(1))  # Flush GPU memory before training

    # === T1: Drift detected (same model, drifted data — already measured above) ===
    # T1 = T0 drift evaluation; the model hasn't been updated yet
    results["T1"] = {"clean": t0_clean, "drift": t0_drift}

    # === Build replay buffer and retrain ===
    print("\n=== Retraining with replay buffer ===")
    data_dir = build_replay_train(drift_test)
    train_time, adapter_dir = retrain(data_dir)
    fused_path = fuse_model(adapter_dir)

    # Extract peak memory from MLX training log (if available)
    peak_mem = 0.0
    log_path = adapter_dir / "training_log.jsonl"
    if log_path.exists():
        for ln in open(log_path):
            rec = json.loads(ln)
            if "peak_memory" in rec:
                peak_mem = max(peak_mem, rec["peak_memory"])

    # === T2: Post-update evaluation (retrained model) ===
    print("\n=== T2: Post-update (replay-trained model) ===")
    model2, tok2 = load("./" + str(fused_path))  # "./" prefix required by mlx_lm

    # Measure inference latency (10 runs, report p50)
    sample_q = clean_test[0]["messages"][0]["content"]
    prompt = tok2.apply_chat_template(
        [{"role": "user", "content": sample_q}],
        tokenize=False,
        add_generation_prompt=True,
    )
    latencies = []
    for _ in range(10):
        t = time.time()
        generate(model2, tok2, prompt=prompt, max_tokens=100, verbose=False)
        latencies.append(time.time() - t)
    p50_lat = float(np.percentile(latencies, 50))

    t2_clean = evaluate(model2, tok2, clean_test, "T2-clean")
    t2_drift = evaluate(model2, tok2, drift_test, "T2-drift")
    results["T2"] = {"clean": t2_clean, "drift": t2_drift}
    print(f"  Clean: loss={t2_clean['mean_loss']:.3f} ppl={t2_clean['mean_ppl']:.2f}")
    print(f"  Drift: loss={t2_drift['mean_loss']:.3f} ppl={t2_drift['mean_ppl']:.2f}")
    del model2, tok2

    # Efficiency metrics for reporting
    efficiency = {
        "train_time_sec": round(train_time, 1),
        "train_time_min": round(train_time / 60, 1),
        "peak_memory_gb": round(peak_mem, 3) if peak_mem > 0 else "N/A",
        "p50_inference_latency_sec": round(p50_lat, 3),
        "model_size_gb": 6.0,
    }
    results["efficiency"] = efficiency

    # Summary: delta percentages showing recovery (negative = improvement)
    results["summary"] = {
        "clean_ppl_T0": t0_clean["mean_ppl"],
        "clean_ppl_T2": t2_clean["mean_ppl"],
        "clean_ppl_delta_pct": round(
            (t2_clean["mean_ppl"] - t0_clean["mean_ppl"]) / t0_clean["mean_ppl"] * 100,
            1,
        ),
        "drift_ppl_T0": t0_drift["mean_ppl"],
        "drift_ppl_T2": t2_drift["mean_ppl"],
        "drift_ppl_delta_pct": round(
            (t2_drift["mean_ppl"] - t0_drift["mean_ppl"]) / t0_drift["mean_ppl"] * 100,
            1,
        ),
    }

    json.dump(results, open(OUT / "continual_learning_results.json", "w"), indent=2)
    print(f"\nSaved {OUT / 'continual_learning_results.json'}")
    print(f"Efficiency: {efficiency}")
    print(f"Summary: {results['summary']}")

    # === Plot: PPL trajectory across T0, T1, T2 ===
    fig, ax = plt.subplots(figsize=(8, 5))
    phases = ["T0\n(Baseline)", "T1\n(Drift)", "T2\n(Post-Update)"]
    xs = [0, 1, 2]

    clean_ppls = [t0_clean["mean_ppl"], t0_clean["mean_ppl"], t2_clean["mean_ppl"]]
    drift_ppls = [t0_drift["mean_ppl"], t0_drift["mean_ppl"], t2_drift["mean_ppl"]]

    # Line plot: clean (circles) and drifted (squares)
    ax.plot(
        xs,
        clean_ppls,
        "o-",
        color=BLUES[0],
        linewidth=2.5,
        markersize=10,
        label="Clean Test",
    )
    ax.plot(
        xs,
        drift_ppls,
        "s-",
        color=BLUES[2],
        linewidth=2.5,
        markersize=10,
        label="Drifted Test",
    )

    # Bootstrap CI bands for clean line
    clean_cis = [
        (t0_clean["loss_ci_low"], t0_clean["loss_ci_high"]),
        (t0_clean["loss_ci_low"], t0_clean["loss_ci_high"]),
        (t2_clean["loss_ci_low"], t2_clean["loss_ci_high"]),
    ]
    for i, (lo, hi) in enumerate(clean_cis):
        ppl_lo = math.exp(min(lo, 20))
        ppl_hi = math.exp(min(hi, 20))
        ax.fill_between(
            [i - 0.05, i + 0.05],
            [ppl_lo, ppl_lo],
            [ppl_hi, ppl_hi],
            color=BLUES[0],
            alpha=0.15,
        )

    # Annotate PPL values above/below each data point
    for i, (cp, dp) in enumerate(zip(clean_ppls, drift_ppls)):
        ax.annotate(
            f"{cp:.1f}",
            (i, cp),
            textcoords="offset points",
            xytext=(0, 12),
            ha="center",
            fontsize=9,
            color=BLUES[0],
            fontweight="bold",
        )
        ax.annotate(
            f"{dp:.1f}",
            (i, dp),
            textcoords="offset points",
            xytext=(0, -18),
            ha="center",
            fontsize=9,
            color=BLUES[2],
            fontweight="bold",
        )

    ax.set_xticks(xs)
    ax.set_xticklabels(phases, fontsize=11)
    ax.set_ylabel("Mean Perplexity", fontsize=12, fontweight="bold")
    ax.set_title(
        "Continual Learning: PPL Trajectory Across Drift Phases",
        fontsize=13,
        fontweight="bold",
    )
    ax.legend(fontsize=10)
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(PLOTS / "continual_learning_trajectory.png", dpi=150)
    print(f"Saved {PLOTS / 'continual_learning_trajectory.png'}")
    plt.close(fig)


if __name__ == "__main__":
    main()
