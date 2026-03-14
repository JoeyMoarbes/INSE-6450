# STRATOS Adaptation Experiment
# Compares original vs augmented model on the hardest test cases to measure adaptation impact.

# Usage: python adaptation_experiment.py
#        Reads generation_results.json, loads both models, produces before/after comparison.

# Context: Identifies the top-10 highest-loss examples from the original model's generation results,
# then re-evaluates them on the augmented model. Computes per-example deltas and generates a
# bar chart showing improvement/regression on those hard cases.

# Prerequisites:
#   - results/generation_results.json (from evaluate_robustness.py --mode full)
#   - Fused models at ../Milestone 2/fused_model and fused_model_augmented/
#   - pip install mlx mlx-lm numpy matplotlib

import json, math, time
from pathlib import Path  # Cross-platform paths

import numpy as np  # Numerical operations
import matplotlib.pyplot as plt  # Plotting
import mlx.core as mx  # Apple Silicon ML framework
import mlx.nn as nn  # Neural network modules (cross-entropy)
from mlx_lm import load, generate  # Model loading + generation

# Paths
ORIG_MODEL = Path("../Milestone 2/fused_model")  # Original model from M2
AUG_MODEL = Path("fused_model_augmented")  # Augmented model from M3
RES = Path("results")  # Input/output directory
PLOTS = Path("plots")  # Plot output
BLUES = ["#1a5276", "#2e86c1", "#5dade2", "#85c1e9", "#d4e6f1"]  # Blue palette
TOP_K = 10  # Number of hardest examples to re-evaluate
MAX_TOKENS = 150  # Cap generation length


def _log_softmax(x: mx.array) -> mx.array:
    return x - mx.logsumexp(x, axis=-1, keepdims=True)  # Manual log-softmax


# Forward pass: loss + perplexity + generation log-prob on a single (question, reference) pair
def score(model, tok, q: str, ref: str) -> dict:
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
    pfx = len(tok.encode(user))
    n_ans = len(full_ids) - pfx

    if n_ans <= 0:
        return {"loss": float("inf"), "ppl": float("inf"), "gen_lp": -999.0}

    # Forward pass on reference
    logits = model(mx.array(full_ids)[None, :])
    loss = nn.losses.cross_entropy(
        logits[0, pfx - 1 : -1, :], mx.array(full_ids[pfx:]), reduction="mean"
    )
    mx.eval(loss)
    l = loss.item()
    del logits, loss

    # Generate and score confidence
    gen = generate(model, tok, prompt=user, max_tokens=MAX_TOKENS, verbose=False)
    glp = -999.0
    if gen.strip():
        gt = tok.apply_chat_template(
            [{"role": "user", "content": q}, {"role": "assistant", "content": gen}],
            tokenize=False,
        )
        gids = tok.encode(gt)
        if len(gids) > pfx + 1:
            gl = model(mx.array(gids)[None, :])
            gs = gl[0, pfx - 1 : -1, :]
            lps = _log_softmax(gs)
            m = mx.mean(
                mx.take_along_axis(lps, mx.array(gids[pfx:])[:, None], axis=-1).squeeze(
                    -1
                )
            )
            mx.eval(m)
            glp = m.item()
            del gl, gs, lps, m

    mx.eval(mx.zeros(1))  # GPU cleanup
    return {"loss": l, "ppl": math.exp(min(l, 20)), "gen_lp": glp, "generated": gen}


def main():
    RES.mkdir(exist_ok=True)
    PLOTS.mkdir(exist_ok=True)

    # Load generation results and pick the hardest examples by loss
    gen_data = json.load(open(RES / "generation_results.json"))
    orig_only = [
        e for e in gen_data if e.get("model") == "original" and e["loss"] < 900
    ]
    orig_only.sort(key=lambda e: e["loss"], reverse=True)  # Highest loss first
    hard = orig_only[:TOP_K]
    print(
        f"Selected {len(hard)} hardest examples (loss range {hard[-1]['loss']:.2f} - {hard[0]['loss']:.2f})"
    )

    # Load both models
    print("Loading original model ...")
    m_orig, t_orig = load(str(ORIG_MODEL))
    print("Loading augmented model ...")
    m_aug, t_aug = load(str(AUG_MODEL))

    # Re-evaluate each hard case on both models
    rows = []
    for i, ex in enumerate(hard):
        q = ex["question"][:500]
        ref = ex["reference"][:500]
        t0 = time.time()
        s_orig = score(m_orig, t_orig, q, ref)  # Score on original model
        s_aug = score(m_aug, t_aug, q, ref)  # Score on augmented model
        dt = time.time() - t0

        row = dict(
            index=i,
            condition=ex.get("condition", "?"),
            question=q[:200],
            orig_loss=s_orig["loss"],
            aug_loss=s_aug["loss"],
            orig_ppl=s_orig["ppl"],
            aug_ppl=s_aug["ppl"],
            orig_glp=s_orig["gen_lp"],
            aug_glp=s_aug["gen_lp"],
            delta_loss=s_aug["loss"] - s_orig["loss"],  # Negative = augmented improved
            delta_ppl=s_aug["ppl"] - s_orig["ppl"],
            elapsed_sec=round(dt, 1),
        )
        rows.append(row)
        print(
            f"  [{i + 1}/{TOP_K}] {row['condition']:15s} orig={s_orig['loss']:.3f} aug={s_aug['loss']:.3f} delta={row['delta_loss']:+.3f}"
        )

    json.dump(rows, open(RES / "adaptation_experiment.json", "w"), indent=2)
    print(f"Saved {RES / 'adaptation_experiment.json'}")

    # Summary statistics
    deltas = [r["delta_loss"] for r in rows]
    improved = sum(1 for d in deltas if d < 0)
    print(f"\nImproved: {improved}/{len(rows)}, mean delta: {np.mean(deltas):+.3f}")

    # Bar chart: per-example loss delta (original vs augmented)
    fig, ax = plt.subplots(figsize=(10, 5))
    xs = range(len(rows))
    colors = [
        BLUES[0] if d < 0 else "#e74c3c" for d in deltas
    ]  # Blue=improved, red=worse
    ax.bar(xs, deltas, color=colors, alpha=0.85)
    ax.axhline(0, color="black", linewidth=0.8)
    ax.set_xticks(xs)
    ax.set_xticklabels(
        [r["condition"][:10] for r in rows], rotation=45, ha="right", fontsize=8
    )
    ax.set_ylabel("Loss Delta (Aug - Orig)", fontsize=11, fontweight="bold")
    ax.set_title(
        f"Adaptation: Top-{TOP_K} Hardest Cases  |  {improved}/{TOP_K} improved",
        fontsize=13,
        fontweight="bold",
    )
    ax.grid(axis="y", alpha=0.3)
    fig.tight_layout()
    fig.savefig(PLOTS / "adaptation_comparison.png", dpi=150)
    print(f"Saved {PLOTS / 'adaptation_comparison.png'}")
    plt.close(fig)


if __name__ == "__main__":
    main()
