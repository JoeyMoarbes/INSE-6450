# STRATOS Active Learning / Human-in-the-Loop Simulation
# Compares AL-selected (uncertainty sampling) vs random selection for replay buffer construction.

# Usage: python hitl_al_experiment.py
#        Produces results/hitl_al_results.json + plots/hitl_al_comparison.png

# Design:
#   1. Score all 500 drift examples with the baseline model (per-example loss = uncertainty).
#   2. AL selection: pick the 250 highest-loss (most uncertain) examples.
#   3. Random selection: pick 250 random examples (same labeling budget).
#   4. Build two replay sets: 70% old clean + 30% AL-selected vs 30% random-selected.
#   5. Retrain both with identical CL config (LoRA rank 16, alpha 32, 100 iters).
#   6. Evaluate both on clean + drift test sets.
#   7. Compare: AL should achieve better drift improvement per labeled example.

# Prerequisites:
#   - Fused model at ../Milestone 2/fused_model
#   - Datasets at ../Milestone 3/datasets/{clean,paraphrase_heavy,vague_keyword}/test.jsonl
#   - Training data at ../Milestone 2/datasets/train.jsonl
#   - pip install mlx mlx-lm numpy matplotlib

import json, math, time, subprocess, shutil
from pathlib import Path  # Cross-platform path handling

import numpy as np  # Array operations, sorting, bootstrapping
import matplotlib  # Plotting backend

matplotlib.use("Agg")  # Non-interactive backend for headless rendering
import matplotlib.pyplot as plt  # Chart generation
import mlx.core as mx  # Apple Silicon ML framework
import mlx.nn as nn  # Neural network modules (cross-entropy loss)
from mlx_lm import load  # Model loading

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


# Score each drift example by its loss — higher loss = more uncertain = more informative.
# This is the acquisition function for pool-based uncertainty sampling (Settles, 2010).
def score_examples(model, tok, exs: list[dict]) -> list[float]:
    scores = []
    for i, ex in enumerate(exs):
        q = ex["messages"][0]["content"]
        ref = ex["messages"][1]["content"]
        m = eval_example(model, tok, q, ref)
        scores.append(m["loss"])
        if (i + 1) % 100 == 0:  # Log progress every 100
            print(f"    Scoring {i + 1}/{len(exs)}")
    return scores


# Build replay training set: 70% old clean + 30% newly-selected examples.
# Simulates the human-in-the-loop step where a domain expert labels the selected batch.
def build_replay(
    old_train: list[dict], new_exs: list[dict], out_dir: Path, valid_path: Path
) -> Path:
    np.random.seed(42)
    np.random.shuffle(old_train)
    n_old = int(len(old_train) * 0.7)  # 70% original training data
    replay_old = old_train[:n_old]
    n_new = min(
        len(new_exs), int(n_old / 0.7 * 0.3)
    )  # 30% from selected drift examples
    replay_new = new_exs[:n_new]
    merged = replay_old + replay_new
    np.random.shuffle(merged)  # Interleave to prevent ordering bias
    save_jsonl(merged, out_dir / "train.jsonl")
    shutil.copy(valid_path, out_dir / "valid.jsonl")  # Reuse original validation set
    print(
        f"  Replay: {len(merged)} examples ({len(replay_old)} old + {len(replay_new)} new)"
    )
    return out_dir


# Run LoRA training via mlx_lm.lora CLI subprocess.
# Uses conservative config to avoid Metal GPU crashes: batch 2, 8 layers, grad-checkpoint.
def retrain(data_dir: Path, adapter_dir: Path) -> float:
    adapter_dir.mkdir(parents=True, exist_ok=True)
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
        "100",  # 100 gradient steps (~0.2 epochs)
        "--val-batches",
        "25",
        "--learning-rate",
        "5e-5",  # Lower LR than initial M2 training (1e-4) for stability
        "--steps-per-report",
        "25",
        "--steps-per-eval",
        "50",
        "--seed",
        "42",  # Reproducibility
        "--grad-checkpoint",  # Trade compute for memory — prevents Metal crashes
    ]
    t0 = time.time()
    result = subprocess.run(cmd, capture_output=True, text=True)
    elapsed = time.time() - t0
    print(result.stdout[-1500:] if len(result.stdout) > 1500 else result.stdout)
    if result.returncode != 0:
        print("STDERR:", result.stderr[-500:])
    return elapsed


# Fuse LoRA adapter weights into the base model to produce a standalone fused model
def fuse(adapter_dir: Path, fused_dir: Path) -> Path:
    cmd = [
        "python",
        "-m",
        "mlx_lm.fuse",
        "--model",
        str(ORIG_MODEL),  # Original base model
        "--adapter-path",
        str(adapter_dir),  # Trained LoRA adapter
        "--save-path",
        str(fused_dir),  # Output fused model directory
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print("Fuse FAILED:", result.stderr[-500:])
    if not fused_dir.exists():
        raise RuntimeError(f"Fused model not found at {fused_dir}")
    return fused_dir


def main():
    OUT.mkdir(exist_ok=True)
    PLOTS.mkdir(exist_ok=True)

    # Load drift pool (500 examples) and clean test set (250 examples)
    drift_all = []
    for p in DRIFT_SETS:
        if p.exists():
            drift_all.extend(load_jsonl(p))
    np.random.seed(42)
    np.random.shuffle(drift_all)
    clean_test = load_jsonl(CLEAN_TEST)
    old_train = load_jsonl(ORIG_TRAIN)
    print(f"Drift pool: {len(drift_all)}, Clean test: {len(clean_test)}")

    # === Step 1: Score all drift examples by uncertainty (per-example loss) ===
    print("\n=== Scoring drift examples (uncertainty) ===")
    model, tok = load(str(ORIG_MODEL))
    scores = score_examples(model, tok, drift_all)

    # Reuse baseline from CL experiment if available, otherwise compute fresh
    q1_path = OUT / "continual_learning_results.json"
    if q1_path.exists():
        q1 = json.load(open(q1_path))
        baseline_clean = q1["T0"]["clean"]
        baseline_drift = q1["T0"]["drift"]
        print(
            f"  Using Q1 baseline: clean PPL={baseline_clean['mean_ppl']:.2f}, drift PPL={baseline_drift['mean_ppl']:.2f}"
        )
    else:
        print("  Computing baseline...")
        baseline_clean = evaluate(model, tok, clean_test, "baseline-clean")
        baseline_drift = evaluate(model, tok, drift_all, "baseline-drift")

    del model, tok
    mx.eval(mx.zeros(1))  # Flush GPU memory

    # === Step 2: AL selection (top-K most uncertain) vs random baseline ===
    k = 250  # "Human labeling budget" — both methods use exactly 250 labels
    ranked = np.argsort(scores)[
        ::-1
    ]  # Sort by loss descending (highest uncertainty first)
    al_indices = ranked[:k]  # AL picks the top-250 most uncertain
    np.random.seed(123)  # Different seed from data shuffle for independence
    rand_indices = np.random.choice(
        len(drift_all), k, replace=False
    )  # Random picks any 250

    al_selected = [drift_all[i] for i in al_indices]
    rand_selected = [drift_all[i] for i in rand_indices]

    al_mean_loss = np.mean([scores[i] for i in al_indices])
    rand_mean_loss = np.mean([scores[i] for i in rand_indices])
    print(f"\n  AL selected: {k} examples, mean loss = {al_mean_loss:.3f}")
    print(f"  Random selected: {k} examples, mean loss = {rand_mean_loss:.3f}")

    results = {
        "selection": {
            "budget": k,
            "pool_size": len(drift_all),
            "al_mean_loss": float(al_mean_loss),
            "rand_mean_loss": float(rand_mean_loss),
        },
        "baseline": {"clean": baseline_clean, "drift": baseline_drift},
    }

    # === Step 3: Build replay sets and retrain (one per selection strategy) ===
    for label, selected in [("al", al_selected), ("random", rand_selected)]:
        print(f"\n=== {label.upper()} selection: retrain ===")
        exp_dir = Path(f"hitl_experiment/{label}")
        data_dir = exp_dir / "data"
        adapter_dir = exp_dir / "adapters"
        fused_dir = exp_dir / "fused_model"

        # Clean any prior run to ensure fresh results
        if exp_dir.exists():
            shutil.rmtree(exp_dir)

        build_replay(list(old_train), selected, data_dir, ORIG_VALID)
        train_time = retrain(data_dir, adapter_dir)
        fuse(adapter_dir, fused_dir)

        # Evaluate retrained model on both test sets
        print(f"\n  Evaluating {label} model...")
        model2, tok2 = load("./" + str(fused_dir))  # "./" prefix required by mlx_lm
        ev_clean = evaluate(model2, tok2, clean_test, f"{label}-clean")
        ev_drift = evaluate(model2, tok2, drift_all, f"{label}-drift")
        del model2, tok2
        mx.eval(mx.zeros(1))  # Flush GPU memory between models

        results[label] = {
            "clean": ev_clean,
            "drift": ev_drift,
            "train_time_sec": round(train_time, 1),
            "n_labeled": k,
        }
        print(
            f"  {label}: clean PPL={ev_clean['mean_ppl']:.2f}, drift PPL={ev_drift['mean_ppl']:.2f}, train={train_time:.1f}s"
        )

    # === Step 4: Summary — compute delta percentages vs baseline ===
    bl_clean_ppl = baseline_clean["mean_ppl"]
    bl_drift_ppl = baseline_drift["mean_ppl"]
    al_clean_ppl = results["al"]["clean"]["mean_ppl"]
    al_drift_ppl = results["al"]["drift"]["mean_ppl"]
    rn_clean_ppl = results["random"]["clean"]["mean_ppl"]
    rn_drift_ppl = results["random"]["drift"]["mean_ppl"]

    results["summary"] = {
        "baseline_clean_ppl": bl_clean_ppl,
        "baseline_drift_ppl": bl_drift_ppl,
        "al_clean_ppl": al_clean_ppl,
        "al_drift_ppl": al_drift_ppl,
        "al_clean_delta_pct": round(  # Negative = improvement
            (al_clean_ppl - bl_clean_ppl) / bl_clean_ppl * 100, 2
        ),
        "al_drift_delta_pct": round(
            (al_drift_ppl - bl_drift_ppl) / bl_drift_ppl * 100, 2
        ),
        "random_clean_ppl": rn_clean_ppl,
        "random_drift_ppl": rn_drift_ppl,
        "random_clean_delta_pct": round(
            (rn_clean_ppl - bl_clean_ppl) / bl_clean_ppl * 100, 2
        ),
        "random_drift_delta_pct": round(
            (rn_drift_ppl - bl_drift_ppl) / bl_drift_ppl * 100, 2
        ),
        "labeling_budget": k,
        "pool_size": len(drift_all),
        "labeling_efficiency": round(k / len(drift_all) * 100, 1),  # % of pool labeled
    }

    json.dump(results, open(OUT / "hitl_al_results.json", "w"), indent=2)
    print(f"\nSaved {OUT / 'hitl_al_results.json'}")
    print(f"Summary: {json.dumps(results['summary'], indent=2)}")

    # === Step 5: Plot — bar chart + uncertainty distribution ===
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    # Left panel: PPL comparison bar chart (Baseline vs Random vs AL)
    ax = axes[0]
    conditions = ["Baseline", "Random\n(250 labeled)", "AL\n(250 labeled)"]
    clean_ppls = [bl_clean_ppl, rn_clean_ppl, al_clean_ppl]
    drift_ppls = [bl_drift_ppl, rn_drift_ppl, al_drift_ppl]
    x = np.arange(len(conditions))
    w = 0.35  # Bar width
    bars1 = ax.bar(x - w / 2, clean_ppls, w, label="Clean Test", color=BLUES[0])
    bars2 = ax.bar(x + w / 2, drift_ppls, w, label="Drifted Test", color=BLUES[2])
    # Annotate each bar with its PPL value
    for b in bars1:
        ax.annotate(
            f"{b.get_height():.1f}",
            (b.get_x() + b.get_width() / 2, b.get_height()),
            textcoords="offset points",
            xytext=(0, 5),
            ha="center",
            fontsize=9,
            color=BLUES[0],
            fontweight="bold",
        )
    for b in bars2:
        ax.annotate(
            f"{b.get_height():.1f}",
            (b.get_x() + b.get_width() / 2, b.get_height()),
            textcoords="offset points",
            xytext=(0, 5),
            ha="center",
            fontsize=9,
            color=BLUES[2],
            fontweight="bold",
        )
    ax.set_xticks(x)
    ax.set_xticklabels(conditions, fontsize=10)
    ax.set_ylabel("Mean Perplexity", fontsize=12, fontweight="bold")
    ax.set_title("Active Learning vs Random Selection", fontsize=13, fontweight="bold")
    ax.legend(fontsize=10, loc="upper left")  # Upper left to avoid covering AL bars
    ax.grid(alpha=0.3, axis="y")

    # Right panel: Uncertainty distribution histogram (AL vs random selected examples)
    ax2 = axes[1]
    al_losses = [scores[i] for i in al_indices]  # Losses of AL-selected examples
    rand_losses = [
        scores[i] for i in rand_indices
    ]  # Losses of randomly selected examples
    ax2.hist(
        rand_losses,
        bins=30,
        alpha=0.6,
        color=BLUES[3],
        label="Random selected",
        density=True,
    )
    ax2.hist(
        al_losses,
        bins=30,
        alpha=0.6,
        color=BLUES[0],
        label="AL selected (top-K)",
        density=True,
    )
    ax2.axvline(  # Pool mean as reference line
        np.mean(scores),
        color="grey",
        linestyle="--",
        linewidth=1.5,
        label=f"Pool mean ({np.mean(scores):.2f})",
    )
    ax2.set_xlabel("Per-Example Loss (Uncertainty)", fontsize=12)
    ax2.set_ylabel("Density", fontsize=12)
    ax2.set_title(
        "AL Selects High-Uncertainty Examples", fontsize=13, fontweight="bold"
    )
    ax2.legend(fontsize=9)
    ax2.grid(alpha=0.3)

    fig.tight_layout()
    fig.savefig(PLOTS / "hitl_al_comparison.png", dpi=150)
    print(f"Saved {PLOTS / 'hitl_al_comparison.png'}")
    plt.close(fig)


if __name__ == "__main__":
    main()
