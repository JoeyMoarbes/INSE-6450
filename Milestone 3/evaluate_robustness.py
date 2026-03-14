# STRATOS Robustness Evaluation
# Evaluates fused models on perturbed test sets, computing loss, perplexity, ROUGE-L, and log-probs.

# Usage: python evaluate_robustness.py --mode eval --model original
#        python evaluate_robustness.py --mode full --model augmented --conditions clean,ood

# Context: Requires MLX framework on Apple Silicon. The script loads each fused model, iterates over
# test conditions (clean, injection, paraphrase, OOD, vague), and computes per-example metrics.
# In eval mode it only computes loss/ppl (fast). In full mode it also generates responses and
# scores them with ROUGE-L, keyword relevance, and generation log-probabilities.

# Prerequisites:
#   - Run generate_perturbed_tests.py first to create datasets/{condition}/test.jsonl
#   - Fused models must exist at ../Milestone 2/fused_model and/or fused_model_augmented/
#   - pip install mlx mlx-lm numpy

import argparse, json, math, time
from pathlib import Path  # Cross-platform file path handling
from typing import Any

import numpy as np  # Numerical operations for metrics and bootstrapping
import mlx.core as mx  # Apple Silicon ML framework
import mlx.nn as nn  # Neural network modules (cross-entropy loss)
from mlx_lm import load, generate  # Model loading and text generation

# Paths to fused models and data
ORIG_MODEL = Path("../Milestone 2/fused_model")  # Original model from Milestone 2
AUG_MODEL = Path("fused_model_augmented")  # Augmented model trained on paraphrased data
DATA_DIR = Path("datasets")  # Perturbed test sets live here
OUT_DIR = Path("results")  # Output JSON files go here
VALID_PATH = Path(
    "../Milestone 2/datasets/valid.jsonl"
)  # Validation set for calibration

# All test conditions the script can evaluate
CONDITIONS = [
    "clean",
    "injection_L1",
    "injection_L2",
    "injection_L3",
    "paraphrase_light",
    "paraphrase_heavy",
    "ood",
    "vague_keyword",
    "vague_phrase",
    "vague_partial",
]

# Domain keywords for topical-relevance scoring (response must contain >= 2)
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
    "abliteration",
    "fine-tune",
    "lora",
    "rlhf",
    "dpo",
    "gcg",
    "autodan",
    "beast",
    "pair",
    "tap",
    "gradient",
    "optimization",
    "perturbation",
    "robustness",
    "vulnerability",
    "exploit",
    "obfuscation",
    "encoding",
    "role-play",
    "asr",
    "success rate",
    "benchmark",
    "toxic",
    "model",
    "training",
}

MAX_TOKENS = 200  # Cap generation length to prevent runaway decoding


def load_jsonl(p: Path) -> list[dict]:
    with open(p) as f:
        return [json.loads(ln) for ln in f if ln.strip()]


# ROUGE-L via word-level longest common subsequence
def rouge_l(pred: str, ref: str) -> float:
    p, r = pred.lower().split(), ref.lower().split()
    if not p or not r:
        return 0.0
    m, n = len(p), len(r)
    dp = [[0] * (n + 1) for _ in range(m + 1)]  # DP table for LCS
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            dp[i][j] = (
                dp[i - 1][j - 1] + 1
                if p[i - 1] == r[j - 1]
                else max(dp[i - 1][j], dp[i][j - 1])
            )
    lcs = dp[m][n]
    if lcs == 0:
        return 0.0
    pr, rc = lcs / m, lcs / n  # Precision and recall
    return 2 * pr * rc / (pr + rc)  # F1


def kw_relevance(text: str) -> tuple[bool, int]:
    t = text.lower()
    cnt = sum(1 for kw in DOMAIN_KW if kw in t)  # Count domain keyword matches
    return cnt >= 2, cnt  # Relevant if 2+ keywords present


def _log_softmax(x: mx.array) -> mx.array:
    # MLX doesn't expose log_softmax directly, so we compute it manually
    return x - mx.logsumexp(x, axis=-1, keepdims=True)


# Eval mode: forward pass to get loss + ppl on reference answer tokens
def eval_loss(model: Any, tok: Any, q: str, ref: str) -> dict:
    # Tokenize full conversation (user + assistant) and user-only prefix
    full = tok.apply_chat_template(
        [{"role": "user", "content": q}, {"role": "assistant", "content": ref}],
        tokenize=False,
    )
    user = tok.apply_chat_template(
        [{"role": "user", "content": q}],
        tokenize=False,
        add_generation_prompt=True,
    )
    full_ids, pfx_len = tok.encode(full), len(tok.encode(user))
    n_ans = len(full_ids) - pfx_len  # Number of answer tokens to score

    if n_ans <= 0:
        return {"loss": float("inf"), "perplexity": float("inf"), "n_answer_tokens": 0}

    logits = model(mx.array(full_ids)[None, :])  # Forward pass
    loss = nn.losses.cross_entropy(  # Loss on answer tokens only
        logits[0, pfx_len - 1 : -1, :],
        mx.array(full_ids[pfx_len:]),
        reduction="mean",
    )
    mx.eval(loss)
    l = loss.item()
    del logits, loss
    mx.eval(mx.zeros(1))  # Force GPU memory cleanup
    return {"loss": l, "perplexity": math.exp(min(l, 20)), "n_answer_tokens": n_ans}


# Full mode: loss + generation + log-probs + ROUGE-L + keyword relevance
def eval_full(model: Any, tok: Any, q: str, ref: str) -> dict:
    # Tokenize conversation
    full = tok.apply_chat_template(
        [{"role": "user", "content": q}, {"role": "assistant", "content": ref}],
        tokenize=False,
    )
    user = tok.apply_chat_template(
        [{"role": "user", "content": q}],
        tokenize=False,
        add_generation_prompt=True,
    )
    full_ids, pfx_len = tok.encode(full), len(tok.encode(user))
    n_ans = len(full_ids) - pfx_len

    if n_ans <= 0:
        return dict(
            loss=float("inf"),
            perplexity=float("inf"),
            ref_mean_logprob=-999,
            gen_mean_logprob=-999,
            generated="",
            rouge_l=0.0,
            keyword_relevant=False,
            keyword_count=0,
            n_answer_tokens=0,
        )

    # Forward pass on reference answer
    logits = model(mx.array(full_ids)[None, :])
    sl = logits[0, pfx_len - 1 : -1, :]  # Shift logits to align with answer labels
    labels = mx.array(full_ids[pfx_len:])
    loss = nn.losses.cross_entropy(sl, labels, reduction="mean")

    lp = _log_softmax(sl)  # Log-probabilities over vocabulary
    ref_lp = mx.mean(
        mx.take_along_axis(lp, labels[:, None], axis=-1).squeeze(-1)
    )  # Mean log-prob of reference tokens
    mx.eval(loss, ref_lp)
    l, rlp = loss.item(), ref_lp.item()
    del logits, sl, lp, loss, ref_lp

    # Generate model response
    gen_text = generate(model, tok, prompt=user, max_tokens=MAX_TOKENS, verbose=False)

    # Compute confidence of generated text (mean per-token log-prob)
    glp = -999.0
    if gen_text.strip():
        gt = tok.apply_chat_template(
            [
                {"role": "user", "content": q},
                {"role": "assistant", "content": gen_text},
            ],
            tokenize=False,
        )
        gids = tok.encode(gt)
        if len(gids) > pfx_len + 1:
            gl = model(mx.array(gids)[None, :])  # Forward pass on generated text
            gs = gl[0, pfx_len - 1 : -1, :]
            glb = mx.array(gids[pfx_len:])
            glps = _log_softmax(gs)
            gm = mx.mean(mx.take_along_axis(glps, glb[:, None], axis=-1).squeeze(-1))
            mx.eval(gm)
            glp = gm.item()
            del gl, gs, glps, gm

    # Score generated output
    rl = rouge_l(gen_text, ref)  # Text overlap with reference
    kr, kc = kw_relevance(gen_text)  # Domain keyword check
    return dict(
        loss=l,
        perplexity=math.exp(min(l, 20)),
        ref_mean_logprob=rlp,
        gen_mean_logprob=glp,
        generated=gen_text,
        rouge_l=rl,
        keyword_relevant=kr,
        keyword_count=kc,
        n_answer_tokens=n_ans,
    )


# Evaluate all examples in a single condition's test.jsonl
def run_condition(model, tok, cond: str, mname: str, mode: str):
    path = DATA_DIR / cond / "test.jsonl"
    if not path.exists():
        return {}, []
    exs = load_jsonl(path)
    fn = (
        eval_loss if mode == "eval" else eval_full
    )  # Pick metric function based on mode
    per_ex, losses = [], []

    for i, ex in enumerate(exs):
        q, ref = ex["messages"][0]["content"], ex["messages"][1]["content"]
        m = fn(model, tok, q, ref)
        m.update(
            index=i, question=q[:500], reference=ref[:500], condition=cond, model=mname
        )
        per_ex.append(m)
        losses.append(m["loss"])
        if (i + 1) % 50 == 0:  # Progress update every 50 examples
            print(f"    [{i + 1}/{len(exs)}] avg_loss={np.mean(losses):.3f}")

    la = np.array(losses)

    # Bootstrap 95% CI on mean loss (1000 resamples, seed 42)
    rng = np.random.default_rng(42)
    boots = [np.mean(rng.choice(la, len(la), replace=True)) for _ in range(1000)]
    lo, hi = np.percentile(boots, [2.5, 97.5])

    # Aggregate results
    agg = dict(
        condition=cond,
        model=mname,
        n=len(exs),
        mean_loss=float(la.mean()),
        mean_ppl=float(np.mean([e["perplexity"] for e in per_ex])),
        loss_ci_low=float(lo),
        loss_ci_high=float(hi),
    )

    # Add generation-level metrics in full mode
    if mode == "full":
        glps = [
            e["gen_mean_logprob"]
            for e in per_ex
            if e.get("gen_mean_logprob", -999) > -50
        ]
        rls = [e["rouge_l"] for e in per_ex if "rouge_l" in e]
        kwn = sum(1 for e in per_ex if e.get("keyword_relevant"))
        agg["mean_gen_logprob"] = float(np.mean(glps)) if glps else None
        agg["mean_rouge_l"] = float(np.mean(rls)) if rls else None
        agg["keyword_relevance_pct"] = kwn / len(exs) * 100
    return agg, per_ex


# Confidence calibration: generate on validation set and set 5th-percentile abstention threshold
def calibrate(model, tok):
    if not VALID_PATH.exists():
        return {}
    exs = load_jsonl(VALID_PATH)
    lps = []  # Collect mean log-prob for each generated response
    for i, ex in enumerate(exs):
        q = ex["messages"][0]["content"]
        prompt = tok.apply_chat_template(
            [{"role": "user", "content": q}], tokenize=False, add_generation_prompt=True
        )
        gen = generate(model, tok, prompt=prompt, max_tokens=MAX_TOKENS, verbose=False)
        if not gen.strip():
            continue

        # Forward pass on generated text to get its mean log-probability
        gt = tok.apply_chat_template(
            [{"role": "user", "content": q}, {"role": "assistant", "content": gen}],
            tokenize=False,
        )
        gids = tok.encode(gt)
        pfx = len(tok.encode(prompt))
        if len(gids) > pfx + 1:
            gl = model(mx.array(gids)[None, :])
            gs = gl[0, pfx - 1 : -1, :]
            glb = mx.array(gids[pfx:])
            g = _log_softmax(gs)
            m = mx.mean(mx.take_along_axis(g, glb[:, None], axis=-1).squeeze(-1))
            mx.eval(m)
            lps.append(m.item())
            del gl, gs, g, m
        if (i + 1) % 50 == 0:
            print(f"  calibrate [{i + 1}/{len(exs)}]")

    thr = float(np.percentile(lps, 5))  # 5th percentile = abstention threshold
    return dict(
        threshold=thr,
        mean_logprob=float(np.mean(lps)),
        p5=thr,
        p10=float(np.percentile(lps, 10)),
        p25=float(np.percentile(lps, 25)),
        p50=float(np.percentile(lps, 50)),
        n_examples=len(lps),
    )


def main():
    # Parse arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", default="full", choices=["eval", "full"])
    ap.add_argument(
        "--model", default="original", choices=["original", "augmented", "both"]
    )
    ap.add_argument("--conditions", default="all")  # Comma-separated list or "all"
    args = ap.parse_args()
    OUT_DIR.mkdir(exist_ok=True)

    # Resolve conditions
    conds = (
        [c for c in CONDITIONS if (DATA_DIR / c / "test.jsonl").exists()]
        if args.conditions == "all"
        else args.conditions.split(",")
    )

    # Resolve models
    models = []
    if args.model in ("original", "both"):
        models.append(("original", ORIG_MODEL))
    if args.model in ("augmented", "both") and AUG_MODEL.exists():
        models.append(("augmented", AUG_MODEL))

    print(f"Mode={args.mode}  Models={[m[0] for m in models]}  Conditions={conds}")
    all_agg, all_ex = [], []

    for mname, mpath in models:
        print(f"\nLoading {mname} from {mpath} ...")
        mdl, tok = load(str(mpath))  # Load fused model + tokenizer

        # Run calibration on original model in full mode only
        if mname == "original" and args.mode == "full":
            cal = calibrate(mdl, tok)
            json.dump(cal, open(OUT_DIR / "confidence_threshold.json", "w"), indent=2)

        # Evaluate each condition
        for cond in conds:
            t0 = time.time()
            agg, pex = run_condition(mdl, tok, cond, mname, args.mode)
            if agg:
                agg["elapsed_sec"] = round(time.time() - t0, 1)
                all_agg.append(agg)
                all_ex.extend(pex)
                print(
                    f"  {cond}: loss={agg['mean_loss']:.3f} ppl={agg['mean_ppl']:.2f} ({agg['elapsed_sec']}s)"
                )
            json.dump(
                all_agg, open(OUT_DIR / "robustness_results.json", "w"), indent=2
            )  # Save incrementally

        del mdl, tok  # Free GPU memory before next model

    # Save per-example results (truncate long text fields to keep file manageable)
    for ex in all_ex:
        for k in ("generated", "reference", "question"):
            if isinstance(ex.get(k), str) and len(ex[k]) > 300:
                ex[k] = ex[k][:300] + "..."
    json.dump(all_ex, open(OUT_DIR / "generation_results.json", "w"), indent=2)
    print(f"\nDone. Results in {OUT_DIR}/")


if __name__ == "__main__":
    main()
