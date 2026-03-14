# STRATOS Monitoring Dashboard
# Simulates a production monitoring pipeline using sliding time windows and statistical drift tests.

# Usage: python monitoring_dashboard.py
#        Reads models/data, computes window metrics, saves JSON + PNG dashboard.

# Context: This script partitions the validation set into 6 time windows and runs each through
# the fused model. It computes per-window loss, perplexity, PSI (population stability index),
# Wasserstein distance, and keyword relevance. A composite health score triggers alerts.

# Prerequisites:
#   - Fused model at ../Milestone 2/fused_model
#   - Validation data at ../Milestone 2/datasets/valid.jsonl
#   - pip install mlx mlx-lm numpy matplotlib scipy

import json, math
from pathlib import Path  # Cross-platform paths

import numpy as np  # Numerical operations
import matplotlib.pyplot as plt  # Plotting
from scipy.stats import wasserstein_distance  # Earth mover's distance for drift
import mlx.core as mx  # Apple Silicon ML framework
import mlx.nn as nn  # Neural network modules (cross-entropy)
from mlx_lm import load, generate  # Model loading + generation

# Paths
MODEL_DIR = Path("../Milestone 2/fused_model")  # Fused model from Milestone 2
VALID = Path("../Milestone 2/datasets/valid.jsonl")  # Validation set
OUT = Path("results")  # JSON output
PLOTS = Path("plots")  # PNG output

BLUES = ["#1a5276", "#2e86c1", "#5dade2", "#85c1e9", "#d4e6f1"]  # Color palette
MAX_TOKENS = 150  # Cap generation length
N_WINDOWS = 6  # Number of simulated time windows
N_BINS = 8  # PSI histogram bins
LAPLACE = 1.0  # Smoothing constant for PSI


def load_jsonl(p: Path) -> list[dict]:
    with open(p) as f:
        return [json.loads(ln) for ln in f if ln.strip()]


# Domain keywords for topical-relevance scoring
DOMAIN_KW = {
    "jailbreak",
    "attack",
    "prompt",
    "injection",
    "adversarial",
    "safety",
    "alignment",
    "llm",
    "language model",
    "token",
    "suffix",
    "bypass",
    "guardrail",
    "red team",
    "defense",
    "harmful",
    "refusal",
}


def _log_softmax(x: mx.array) -> mx.array:
    return x - mx.logsumexp(x, axis=-1, keepdims=True)  # Manual log-softmax


# Compute loss, perplexity, and generation log-prob for one example
def score_example(model, tok, q: str, ref: str) -> dict:
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
        return {
            "loss": float("inf"),
            "ppl": float("inf"),
            "gen_lp": -999.0,
            "kw_hit": False,
        }

    # Forward pass for loss on reference tokens
    logits = model(mx.array(full_ids)[None, :])
    loss = nn.losses.cross_entropy(
        logits[0, pfx - 1 : -1, :], mx.array(full_ids[pfx:]), reduction="mean"
    )
    mx.eval(loss)
    l = loss.item()
    del logits, loss

    # Generate response and score its confidence
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
            glb = mx.array(gids[pfx:])
            lps = _log_softmax(gs)
            m = mx.mean(mx.take_along_axis(lps, glb[:, None], axis=-1).squeeze(-1))
            mx.eval(m)
            glp = m.item()
            del gl, gs, lps, m

    kw = any(
        k in gen.lower() for k in DOMAIN_KW
    )  # Check if response contains domain keywords
    mx.eval(mx.zeros(1))  # Force GPU cleanup
    return {"loss": l, "ppl": math.exp(min(l, 20)), "gen_lp": glp, "kw_hit": kw}


# PSI: measures how a window's loss distribution shifted from the reference
def psi(ref_vals: np.ndarray, win_vals: np.ndarray) -> float:
    lo = min(ref_vals.min(), win_vals.min()) - 1e-6
    hi = max(ref_vals.max(), win_vals.max()) + 1e-6
    edges = np.linspace(lo, hi, N_BINS + 1)
    ref_h = (
        np.histogram(ref_vals, bins=edges)[0].astype(float) + LAPLACE
    )  # Laplace smoothing
    win_h = np.histogram(win_vals, bins=edges)[0].astype(float) + LAPLACE
    ref_p = ref_h / ref_h.sum()  # Normalize to proportions
    win_p = win_h / win_h.sum()
    return float(np.sum((win_p - ref_p) * np.log(win_p / ref_p)))  # PSI formula


# Composite health score: weighted combination of metrics (0=bad, 100=good)
def health_score(losses: list, psi_val: float, kw_pct: float) -> float:
    ml = np.mean(losses)
    loss_s = max(0, 100 - (ml - 2.0) * 50)  # Penalty ramps above loss=2.0
    psi_s = max(0, 100 - psi_val * 200)  # Penalty ramps above PSI=0.5
    kw_s = kw_pct  # Keyword relevance already in 0-100
    return float(0.4 * loss_s + 0.3 * psi_s + 0.3 * kw_s)  # Weighted sum


def main():
    OUT.mkdir(exist_ok=True)
    PLOTS.mkdir(exist_ok=True)

    print("Loading model ...")
    model, tok = load(str(MODEL_DIR))

    exs = load_jsonl(VALID)
    np.random.seed(42)
    np.random.shuffle(exs)  # Shuffle to simulate temporal ordering
    wsize = len(exs) // N_WINDOWS  # Examples per window

    # Score all examples in reference window (window 0) to get baseline distribution
    ref_exs = exs[:wsize]
    ref_scores = []
    for i, ex in enumerate(ref_exs):
        q, r = ex["messages"][0]["content"], ex["messages"][1]["content"]
        ref_scores.append(score_example(model, tok, q, r))
        if (i + 1) % 20 == 0:
            print(f"  ref [{i + 1}/{wsize}]")
    ref_losses = np.array([s["loss"] for s in ref_scores])

    # Iterate through all windows and compute monitoring metrics
    windows = []
    for w in range(N_WINDOWS):
        start = w * wsize
        chunk = exs[start : start + wsize]
        scores = []
        for i, ex in enumerate(chunk):
            q, r = ex["messages"][0]["content"], ex["messages"][1]["content"]
            scores.append(score_example(model, tok, q, r))
            if (i + 1) % 20 == 0:
                print(f"  win {w} [{i + 1}/{len(chunk)}]")

        losses = np.array([s["loss"] for s in scores])
        lps = [s["gen_lp"] for s in scores if s["gen_lp"] > -50]
        kw_pct = (
            sum(1 for s in scores if s["kw_hit"]) / len(scores) * 100
        )  # % with domain keywords

        p = psi(ref_losses, losses)  # Distribution shift from reference
        wd = float(wasserstein_distance(ref_losses, losses))  # Earth mover's distance
        hs = health_score(losses.tolist(), p, kw_pct)  # Composite health

        rec = dict(
            window=w,
            n=len(chunk),
            mean_loss=float(losses.mean()),
            std_loss=float(losses.std()),
            mean_ppl=float(np.mean([s["ppl"] for s in scores])),
            mean_gen_lp=float(np.mean(lps)) if lps else None,
            kw_relevance_pct=round(kw_pct, 1),
            psi=round(p, 4),
            wasserstein=round(wd, 4),
            health_score=round(hs, 1),
            alert="ALERT" if hs < 60 else "OK",  # Flag windows needing attention
        )
        windows.append(rec)
        print(
            f"  Window {w}: loss={rec['mean_loss']:.3f} psi={p:.4f} health={hs:.1f} {rec['alert']}"
        )

    json.dump(windows, open(OUT / "monitoring_metrics.json", "w"), indent=2)
    print(f"Saved {OUT / 'monitoring_metrics.json'}")

    # Plot 4-panel dashboard
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    ws = [w["window"] for w in windows]

    # Panel 1: Mean loss per window with alert markers
    ax = axes[0][0]
    ax.plot(ws, [w["mean_loss"] for w in windows], "o-", color=BLUES[0], linewidth=2)
    for w in windows:
        if w["alert"] == "ALERT":
            ax.plot(
                w["window"], w["mean_loss"], "rv", markersize=12
            )  # Red triangle on alerts
    ax.set_title("Mean Loss per Window", fontweight="bold")
    ax.set_xlabel("Window")
    ax.set_ylabel("Loss")
    ax.grid(alpha=0.3)

    # Panel 2: PSI drift over time
    ax = axes[0][1]
    ax.bar(ws, [w["psi"] for w in windows], color=BLUES[2], alpha=0.8)
    ax.axhline(
        0.2, color="orange", linestyle="--", label="Moderate drift"
    )  # PSI > 0.2 = moderate
    ax.axhline(
        0.5, color="red", linestyle="--", label="Severe drift"
    )  # PSI > 0.5 = severe
    ax.set_title("PSI (Distribution Shift)", fontweight="bold")
    ax.set_xlabel("Window")
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3)

    # Panel 3: Composite health score
    ax = axes[1][0]
    colors = [
        BLUES[0] if w["health_score"] >= 60 else "#e74c3c" for w in windows
    ]  # Red if unhealthy
    ax.bar(ws, [w["health_score"] for w in windows], color=colors, alpha=0.85)
    ax.axhline(60, color="orange", linestyle="--", label="Alert threshold")
    ax.set_title("Health Score", fontweight="bold")
    ax.set_xlabel("Window")
    ax.set_ylim(0, 100)
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3)

    # Panel 4: Keyword relevance trend
    ax = axes[1][1]
    ax.plot(
        ws, [w["kw_relevance_pct"] for w in windows], "s-", color=BLUES[1], linewidth=2
    )
    ax.set_title("Keyword Relevance %", fontweight="bold")
    ax.set_xlabel("Window")
    ax.set_ylabel("%")
    ax.set_ylim(0, 100)
    ax.grid(alpha=0.3)

    fig.suptitle("STRATOS Monitoring Dashboard", fontsize=15, fontweight="bold")
    fig.tight_layout(rect=[0, 0, 1, 0.96])
    fig.savefig(PLOTS / "monitoring_dashboard.png", dpi=150)
    print(f"Saved {PLOTS / 'monitoring_dashboard.png'}")
    plt.close(fig)


if __name__ == "__main__":
    main()
