# STRATOS Robustness Plots
# Generates bar charts, confidence histograms, and reliability diagram from evaluation results.

# Usage: python robustness_plots.py
#        Reads from results/ and writes PNG files to plots/

# Context: Run evaluate_robustness.py first (both eval and full modes) to populate results/.
# Plots use a blue palette consistent with Milestone 2 visuals.

# Prerequisites:
#   - results/robustness_results.json (from evaluate_robustness.py --mode eval --model both)
#   - results/generation_results.json (from evaluate_robustness.py --mode full)
#   - results/confidence_threshold.json (from evaluate_robustness.py --mode full)
#   - pip install matplotlib numpy

import json
from pathlib import Path  # Cross-platform file paths

import matplotlib.pyplot as plt  # Plotting library
import numpy as np  # Numerical operations

# Blue palette matching Milestone 2 visuals
BLUES = ["#1a5276", "#2e86c1", "#5dade2", "#85c1e9", "#d4e6f1"]
RES = Path("results")  # Where evaluation outputs live
PLOTS = Path("plots")  # Where to save plot PNGs

# Short display labels for each test condition
NICE = {
    "clean": "Clean",
    "injection_L1": "Inject-L1",
    "injection_L2": "Inject-L2",
    "injection_L3": "Inject-L3",
    "paraphrase_light": "Para-Light",
    "paraphrase_heavy": "Para-Heavy",
    "ood": "OOD",
    "vague_keyword": "Vague-KW",
    "vague_phrase": "Vague-Phr",
    "vague_partial": "Vague-Part",
}


# Grouped bar chart: per-condition perplexity + mean loss for both models
def plot_bar():
    data = json.load(open(RES / "robustness_results.json"))

    # Separate results by model name
    orig = {d["condition"]: d for d in data if d["model"] == "original"}
    aug = {d["condition"]: d for d in data if d["model"] == "augmented"}
    conds = list(orig.keys())  # Use condition order from original model
    x = np.arange(len(conds))
    w = 0.35  # Bar width

    fig, ax1 = plt.subplots(figsize=(14, 6))

    # Perplexity bars (left axis)
    o_ppl = [orig[c]["mean_ppl"] for c in conds]
    a_ppl = [aug[c]["mean_ppl"] for c in conds] if aug else []
    ax1.bar(x - w / 2, o_ppl, w, label="Original PPL", color=BLUES[0], alpha=0.85)
    if a_ppl:
        ax1.bar(x + w / 2, a_ppl, w, label="Augmented PPL", color=BLUES[2], alpha=0.85)

    # Error bars from bootstrap CI
    for i, c in enumerate(conds):
        lo = orig[c].get("loss_ci_low", orig[c]["mean_loss"])
        hi = orig[c].get("loss_ci_high", orig[c]["mean_loss"])
        ax1.errorbar(
            i - w / 2,
            o_ppl[i],
            yerr=max(hi - lo, 0) * 5,
            color="black",  # Scaled CI for visibility
            capsize=3,
            linewidth=1,
            fmt="none",
        )
        if aug and c in aug:
            lo2 = aug[c].get("loss_ci_low", aug[c]["mean_loss"])
            hi2 = aug[c].get("loss_ci_high", aug[c]["mean_loss"])
            ax1.errorbar(
                i + w / 2,
                a_ppl[i],
                yerr=max(hi2 - lo2, 0) * 5,
                color="black",
                capsize=3,
                linewidth=1,
                fmt="none",
            )

    ax1.set_ylabel("Perplexity", fontsize=12, fontweight="bold")
    ax1.set_xticks(x)
    ax1.set_xticklabels([NICE.get(c, c) for c in conds], rotation=30, ha="right")

    # Mean loss line (right axis)
    ax2 = ax1.twinx()
    o_loss = [orig[c]["mean_loss"] for c in conds]
    ax2.plot(
        x, o_loss, "o-", color=BLUES[1], label="Orig Loss", linewidth=2, markersize=6
    )
    if aug:
        a_loss = [aug[c]["mean_loss"] for c in conds]
        ax2.plot(
            x,
            a_loss,
            "s--",
            color=BLUES[3],
            label="Aug Loss",
            linewidth=2,
            markersize=6,
        )
    ax2.set_ylabel("Mean Loss", fontsize=12, fontweight="bold")

    # Combine legends from both axes
    h1, l1 = ax1.get_legend_handles_labels()
    h2, l2 = ax2.get_legend_handles_labels()
    ax1.legend(h1 + h2, l1 + l2, loc="upper left", fontsize=9)
    ax1.set_title(
        "Robustness: Perplexity & Loss by Condition", fontsize=14, fontweight="bold"
    )
    ax1.grid(axis="y", alpha=0.3)
    fig.tight_layout()
    fig.savefig(PLOTS / "robustness_bar_chart.png", dpi=150)
    print("Saved robustness_bar_chart.png")
    plt.close(fig)


# Confidence histograms: distribution of generation log-probs across conditions
def plot_confidence():
    data = json.load(open(RES / "generation_results.json"))
    cal = json.load(open(RES / "confidence_threshold.json"))
    thr = cal.get("threshold", -2.5)  # Abstention threshold from calibration

    # Group gen_mean_logprob values by condition
    cond_lps = {}
    for e in data:
        if e.get("gen_mean_logprob") and e["gen_mean_logprob"] > -50:
            cond_lps.setdefault(e["condition"], []).append(e["gen_mean_logprob"])

    conds = sorted(cond_lps.keys())
    ncols = min(3, len(conds))
    nrows = (len(conds) + ncols - 1) // ncols  # Ceiling division
    fig, axes = plt.subplots(
        nrows, ncols, figsize=(5 * ncols, 4 * nrows), squeeze=False
    )

    for idx, cond in enumerate(conds):
        ax = axes[idx // ncols][idx % ncols]
        vals = np.array(cond_lps[cond])
        ax.hist(
            vals, bins=25, color=BLUES[2], alpha=0.7, edgecolor=BLUES[0]
        )  # Log-prob histogram
        ax.axvline(
            thr, color="red", linestyle="--", linewidth=1.5, label=f"thr={thr:.2f}"
        )  # Threshold line
        pct_below = np.mean(vals < thr) * 100  # Percentage flagged for abstention
        ax.set_title(
            f"{NICE.get(cond, cond)} ({pct_below:.0f}% < thr)",
            fontsize=10,
            fontweight="bold",
        )
        ax.set_xlabel("Mean log-prob")
        ax.legend(fontsize=8)
        ax.grid(alpha=0.3)

    # Hide unused subplots
    for idx in range(len(conds), nrows * ncols):
        axes[idx // ncols][idx % ncols].set_visible(False)

    fig.suptitle(
        "Generation Confidence by Condition", fontsize=14, fontweight="bold", y=1.01
    )
    fig.tight_layout()
    fig.savefig(PLOTS / "confidence_histograms.png", dpi=150, bbox_inches="tight")
    print("Saved confidence_histograms.png")
    plt.close(fig)


# Reliability diagram: predicted confidence vs observed accuracy in equally-spaced bins
def plot_reliability():
    data = json.load(open(RES / "generation_results.json"))

    # Extract confidence (log-prob) and correctness (ROUGE-L > 0.3)
    confs, accs = [], []
    for e in data:
        if e.get("gen_mean_logprob") and e["gen_mean_logprob"] > -50 and "rouge_l" in e:
            confs.append(e["gen_mean_logprob"])
            accs.append(
                1 if e["rouge_l"] > 0.3 else 0
            )  # Binary accuracy: ROUGE-L > 0.3

    if not confs:
        print("No data for reliability diagram")
        return

    confs, accs = np.array(confs), np.array(accs)
    nbins = 10  # Number of calibration bins
    bins = np.linspace(confs.min(), confs.max(), nbins + 1)
    bin_accs, bin_confs, bin_ns = [], [], []

    for i in range(nbins):
        mask = (confs >= bins[i]) & (confs < bins[i + 1])
        if mask.sum() > 0:
            bin_accs.append(accs[mask].mean())  # Observed accuracy in this bin
            bin_confs.append(confs[mask].mean())  # Mean predicted confidence
            bin_ns.append(mask.sum())

    fig, ax = plt.subplots(figsize=(7, 6))
    xs = np.array(bin_confs)
    ys = np.array(bin_accs)
    ns = np.array(bin_ns)

    ax.bar(
        xs,
        ys,
        width=(bins[1] - bins[0]) * 0.8,
        alpha=0.7,  # Accuracy bars
        color=BLUES[2],
        edgecolor=BLUES[0],
        label="Accuracy",
    )
    ax.plot(
        [confs.min(), confs.max()], [0, 1], "k--", alpha=0.5, label="Perfect cal."
    )  # Diagonal = perfect

    # Annotate each bar with sample count
    for x, y, n in zip(xs, ys, ns):
        ax.annotate(f"n={n}", (x, y + 0.02), ha="center", fontsize=7, color=BLUES[0])

    # ECE = mean absolute gap between predicted confidence and observed accuracy
    ece = float(
        np.average(np.abs(ys - (xs - xs.min()) / (xs.max() - xs.min())), weights=ns)
    )
    ax.set_title(
        f"Reliability Diagram  |  ECE = {ece:.3f}", fontsize=13, fontweight="bold"
    )
    ax.set_xlabel("Mean log-prob (confidence)", fontsize=11)
    ax.set_ylabel("Observed accuracy (ROUGE-L > 0.3)", fontsize=11)
    ax.legend(fontsize=10)
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(PLOTS / "reliability_diagram.png", dpi=150)
    print("Saved reliability_diagram.png")
    plt.close(fig)


if __name__ == "__main__":
    PLOTS.mkdir(exist_ok=True)
    plot_bar()

    # Only generate confidence/reliability plots if full-mode results exist
    gen_path = RES / "generation_results.json"
    if gen_path.exists() and json.load(open(gen_path)):
        plot_confidence()
        plot_reliability()
    else:
        print("Skipping confidence/reliability (no generation_results.json)")
