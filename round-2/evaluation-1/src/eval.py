#!/usr/bin/env python3
"""
Statistical Analysis of Self-Check Divergence
Evaluates experiment results to test whether shorter chain-of-thought reduces contradiction.
"""

import json
import math
import re
import resource
import sys
import gc
from pathlib import Path
from typing import Any
from collections import defaultdict

import numpy as np
from scipy import stats
from loguru import logger

# Configure logging
logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
logger.add("logs/run.log", rotation="30 MB", level="DEBUG")

# ============================================================
# CONFIGURATION
# ============================================================

EXPERIMENT_LOG = Path("/ai-inventor/aii_data/runs/run_DyrN7YJjJoEX/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/logs/run.log")
GSM8K_DATA = Path("/ai-inventor/aii_data/runs/run_DyrN7YJjJoEX/3_invention_loop/iter_1/gen_art/gen_art_dataset_1/full_data_out.json")
OUTPUT_FILE = Path("eval_out.json")

BOOTSTRAP_ITERATIONS = 1000
CI_LEVEL = 0.95

# ============================================================
# HARDWARE DETECTION
# ============================================================

def _detect_cpus() -> int:
    try:
        parts = Path("/sys/fs/cgroup/cpu.max").read_text().split()
        if parts[0] != "max":
            return math.ceil(int(parts[0]) / int(parts[1]))
    except (FileNotFoundError, ValueError):
        pass
    try:
        q = int(Path("/sys/fs/cgroup/cpu/cpu.cfs_quota_us").read_text())
        p = int(Path("/sys/fs/cgroup/cpu/cpu.cfs_period_us").read_text())
        if q > 0:
            return math.ceil(q / p)
    except (FileNotFoundError, ValueError):
        pass
    try:
        return len(os.sched_getaffinity(0))
    except (AttributeError, OSError):
        pass
    return 1

def _container_ram_gb() -> float | None:
    for p in ["/sys/fs/cgroup/memory.max", "/sys/fs/cgroup/memory/memory.limit_in_bytes"]:
        try:
            v = Path(p).read_text().strip()
            if v != "max" and int(v) < 1_000_000_000_000:
                return int(v) / 1e9
        except (FileNotFoundError, ValueError):
            pass
    return None

import os
NUM_CPUS = _detect_cpus()
TOTAL_RAM_GB = _container_ram_gb() or 14.0
AVAILABLE_RAM_GB = min(4.0, TOTAL_RAM_GB * 0.3)

logger.info(f"Detected {NUM_CPUS} CPUs, {TOTAL_RAM_GB:.1f}GB RAM (limit)")

# ============================================================
# DATA LOADING
# ============================================================

def parse_experiment_log(log_path: Path) -> list[dict]:
    """Parse experiment log to extract results."""
    results = []
    
    with open(log_path, "r") as f:
        for line in f:
            match = re.search(
                r"Problem (\d+), (\w+): agreement=(True|False), cot_acc=(True|False), sc_acc=(True|False), cost=\$([\d.]+)",
                line
            )
            if match:
                results.append({
                    "problem_index": int(match.group(1)),
                    "cot_style": match.group(2),
                    "agreement": match.group(3) == "True",
                    "cot_correct": match.group(4) == "True",
                    "selfcheck_correct": match.group(5) == "True",
                    "cumulative_cost": float(match.group(6)),
                })
    
    logger.info(f"Parsed {len(results)} results from log")
    return results


def load_gsm8k_data(data_path: Path) -> dict[int, dict]:
    """Load GSM8K data and return dict mapping problem index to metadata."""
    logger.info(f"Loading GSM8K data from {data_path}")
    
    with open(data_path, "r") as f:
        data = json.load(f)
    
    examples = data["datasets"][0]["examples"]
    problem_map = {}
    
    for ex in examples:
        idx = ex["metadata_row_index"]
        problem_map[idx] = {
            "input": ex["input"],
            "output": ex["output"],
            "difficulty_tier": ex["metadata_difficulty_tier"],
            "difficulty_score": ex["metadata_difficulty_score"],
            "solution_steps": ex["metadata_solution_steps"],
            "operation_count": ex["metadata_operation_count"],
            "numeric_count": ex["metadata_numeric_count"],
            "sentence_count": ex["metadata_sentence_count"],
            "token_count": ex["metadata_token_count"],
            "multi_step_indicators": ex["metadata_multi_step_indicators"],
            "split": ex["metadata_split"],
        }
    
    logger.info(f"Loaded {len(problem_map)} GSM8K problems")
    return problem_map


# ============================================================
# ANALYSIS FUNCTIONS
# ============================================================

def validate_difficulty(results: list[dict], problem_map: dict[int, dict]) -> dict:
    """Validate difficulty stratification by computing accuracy per tier."""
    tier_data = defaultdict(lambda: {"correct": 0, "total": 0})
    
    for r in results:
        idx = r["problem_index"]
        if idx in problem_map:
            tier = problem_map[idx]["difficulty_tier"]
            tier_data[tier]["total"] += 1
            if r["cot_correct"]:
                tier_data[tier]["correct"] += 1
    
    metrics = {}
    for tier in ["easy", "medium", "hard"]:
        data = tier_data[tier]
        if data["total"] > 0:
            metrics[f"{tier}_accuracy"] = round(data["correct"] / data["total"], 4)
            metrics[f"{tier}_count"] = data["total"]
        else:
            metrics[f"{tier}_accuracy"] = 0.0
            metrics[f"{tier}_count"] = 0
    
    # Check monotonicity
    easy_acc = metrics["easy_accuracy"]
    medium_acc = metrics["medium_accuracy"]
    hard_acc = metrics["hard_accuracy"]
    metrics["monotonic"] = easy_acc > medium_acc > hard_acc
    
    logger.info(f"Difficulty validation: easy={easy_acc:.3f}, medium={medium_acc:.3f}, hard={hard_acc:.3f}, monotonic={metrics['monotonic']}")
    
    return metrics


def compute_bootstrap_ci(agreement_rates: dict[str, float], n_per_style: dict[str, int]) -> dict:
    """Compute 95% confidence intervals via bootstrap resampling."""
    result = {}
    
    for style in ["short", "medium", "long"]:
        # We don't have raw agreement values, so we simulate bootstrap from binomial
        # Using the observed rate and count to generate bootstrap samples
        n = n_per_style.get(style, 0)
        if n == 0:
            result[style] = {"mean": 0.0, "ci_lower": 0.0, "ci_upper": 1.0}
            continue
        
        rate = agreement_rates[style]
        n_success = int(round(rate * n))
        
        # Bootstrap resampling
        resampled_means = []
        for _ in range(BOOTSTRAP_ITERATIONS):
            sample = np.random.binomial(1, rate, n)
            resampled_means.append(np.mean(sample))
        
        ci_lower = float(np.percentile(resampled_means, (1 - CI_LEVEL) / 2 * 100))
        ci_upper = float(np.percentile(resampled_means, (1 + CI_LEVEL) / 2 * 100))
        
        result[style] = {
            "mean": round(rate, 4),
            "ci_lower": round(ci_lower, 4),
            "ci_upper": round(ci_upper, 4),
            "n": n
        }
    
    return result


def compute_mcnemar_test(results: list[dict]) -> dict:
    """McNemar's test comparing short vs long CoT agreement."""
    # Group by problem index
    problem_results = defaultdict(dict)
    for r in results:
        problem_results[r["problem_index"]][r["cot_style"]] = r["agreement"]
    
    # Build 2x2 contingency table
    # Rows: short agreement (agree/disagree), Cols: long agreement (agree/disagree)
    a = 0  # short agree, long agree
    b = 0  # short agree, long disagree
    c = 0  # short disagree, long agree
    d = 0  # short disagree, long disagree
    
    for idx, styles in problem_results.items():
        if "short" in styles and "long" in styles:
            short_agree = styles["short"]
            long_agree = styles["long"]
            if short_agree and long_agree:
                a += 1
            elif short_agree and not long_agree:
                b += 1
            elif not short_agree and long_agree:
                c += 1
            else:
                d += 1
    
    # McNemar's chi-squared (without continuity correction)
    if b + c > 0:
        chi2 = (b - c) ** 2 / (b + c)
        p_value = float(stats.chi2.sf(chi2, 1))
    else:
        chi2 = 0.0
        p_value = 1.0
    
    return {
        "chi2": round(chi2, 4),
        "p_value": round(p_value, 6),
        "discordant_pairs": {"b": b, "c": c},
        "concordant_pairs": {"a": a, "d": d}
    }


def compute_paired_sign_test(results: list[dict]) -> dict:
    """Paired sign test for short vs long agreement."""
    problem_results = defaultdict(dict)
    for r in results:
        problem_results[r["problem_index"]][r["cot_style"]] = r["agreement"]
    
    positive = 0  # long > short
    negative = 0  # long < short
    tied = 0
    
    for idx, styles in problem_results.items():
        if "short" in styles and "long" in styles:
            short_agree = styles["short"]
            long_agree = styles["long"]
            if long_agree and not short_agree:
                positive += 1
            elif not long_agree and short_agree:
                negative += 1
            else:
                tied += 1
    
    n_effective = positive + negative
    if n_effective > 0:
        # Use binomial test: under null, P(positive) = 0.5
        p_value = 2 * min(stats.binom.cdf(positive, n_effective, 0.5),
                          1 - stats.binom.cdf(positive - 1, n_effective, 0.5))
        z = (positive - n_effective / 2) / (n_effective / 4) ** 0.5 if n_effective > 0 else 0
    else:
        p_value = 1.0
        z = 0.0
    
    return {
        "z": round(z, 4),
        "p_value": round(p_value, 6),
        "positive_differences": positive,
        "negative_differences": negative,
        "tied": tied,
        "n_effective": n_effective
    }


def compute_spearman_trend(results: list[dict]) -> dict:
    """Spearman correlation between CoT length and agreement rate."""
    # Group by problem and style, create paired data
    length_map = {"short": 1, "medium": 2, "long": 3}
    
    problem_agreements = defaultdict(dict)
    for r in results:
        problem_agreements[r["problem_index"]][r["cot_style"]] = 1 if r["agreement"] else 0
    
    # Create arrays for correlation
    lengths = []
    agreements = []
    for idx, style_agreements in problem_agreements.items():
        for style, agree in style_agreements.items():
            if style in length_map:
                lengths.append(length_map[style])
                agreements.append(agree)
    
    if len(lengths) < 3:
        return {"spearman_r": 0.0, "p_value": 1.0}
    
    spearman_r, p_value = stats.spearmanr(lengths, agreements)
    
    return {
        "spearman_r": round(float(spearman_r), 4),
        "p_value": round(float(p_value), 6)
    }


def compute_divergence(results: list[dict]) -> dict:
    """Compute divergence between accuracy and agreement rates."""
    by_style = defaultdict(lambda: {"acc": [], "agree": []})
    
    for r in results:
        style = r["cot_style"]
        by_style[style]["acc"].append(1 if r["cot_correct"] else 0)
        by_style[style]["agree"].append(1 if r["agreement"] else 0)
    
    divergence = {}
    for style in ["short", "medium", "long"]:
        if style in by_style:
            acc_rate = np.mean(by_style[style]["acc"])
            agree_rate = np.mean(by_style[style]["agree"])
            divergence[style] = {
                "accuracy": round(float(acc_rate), 4),
                "agreement": round(float(agree_rate), 4),
                "divergence": round(float(agree_rate - acc_rate), 4)
            }
        else:
            divergence[style] = {"accuracy": 0.0, "agreement": 0.0, "divergence": 0.0}
    
    return divergence


def compute_effect_sizes(mcnemar: dict, sign_test: dict, agreement_rates: dict[str, float]) -> dict:
    """Compute Cohen's h and odds ratio."""
    # Cohen's h for short vs long
    p1 = agreement_rates.get("short", 0)
    p2 = agreement_rates.get("long", 0)
    
    if p1 > 0 and p2 > 0:
        cohens_h = abs(2 * math.asin(math.sqrt(p1)) - 2 * math.asin(math.sqrt(p2)))
    else:
        cohens_h = 0.0
    
    # Odds ratio from McNemar's
    discordant_b = mcnemar.get("discordant_pairs", {}).get("b", 0)
    discordant_c = mcnemar.get("discordant_pairs", {}).get("c", 0)
    
    if discordant_c > 0:
        odds_ratio = discordant_b / discordant_c
    else:
        odds_ratio = float('inf') if discordant_b > 0 else 1.0
    
    return {
        "cohens_h_short_vs_long": round(float(cohens_h), 4),
        "odds_ratio_mcnemar": round(float(odds_ratio), 4) if odds_ratio != float('inf') else "inf",
        "interpretation": "small" if cohens_h < 0.2 else ("medium" if cohens_h < 0.5 else "large")
    }


def stratified_analysis(results: list[dict], problem_map: dict[int, dict]) -> dict:
    """Perform analysis stratified by difficulty tier."""
    tier_data = defaultdict(lambda: defaultdict(lambda: {"agree": [], "correct": []}))
    
    for r in results:
        idx = r["problem_index"]
        if idx in problem_map:
            tier = problem_map[idx]["difficulty_tier"]
            style = r["cot_style"]
            tier_data[tier][style]["agree"].append(1 if r["agreement"] else 0)
            tier_data[tier][style]["correct"].append(1 if r["cot_correct"] else 0)
    
    stratified = {}
    for tier in ["easy", "medium", "hard"]:
        stratified[tier] = {}
        for style in ["short", "medium", "long"]:
            data = tier_data[tier][style]
            if data["agree"]:
                stratified[tier][style] = {
                    "agreement_rate": round(float(np.mean(data["agree"])), 4),
                    "accuracy": round(float(np.mean(data["correct"])), 4),
                    "n": len(data["agree"])
                }
            else:
                stratified[tier][style] = {"agreement_rate": 0.0, "accuracy": 0.0, "n": 0}
    
    return stratified


# ============================================================
# MAIN
# ============================================================

@logger.catch(reraise=True)
def main():
    """Main evaluation function."""
    # Set memory limit
    ram_budget = int(AVAILABLE_RAM_GB * 1024**3)
    resource.setrlimit(resource.RLIMIT_AS, (ram_budget * 3, ram_budget * 3))
    
    # Load data
    logger.info("=" * 60)
    logger.info("Loading experiment data")
    logger.info("=" * 60)
    
    results = parse_experiment_log(EXPERIMENT_LOG)
    problem_map = load_gsm8k_data(GSM8K_DATA)
    
    if not results:
        logger.error("No results found in experiment log")
        sys.exit(1)
    
    # Group results by style
    by_style = defaultdict(list)
    for r in results:
        by_style[r["cot_style"]].append(r)
    
    n_per_style = {style: len(group) for style, group in by_style.items()}
    agreement_rates = {style: sum(1 for r in group if r["agreement"]) / len(group) 
                       for style, group in by_style.items()}
    
    logger.info(f"Results by style: {n_per_style}")
    logger.info(f"Agreement rates: {agreement_rates}")
    
    # Perform analyses
    logger.info("=" * 60)
    logger.info("Running statistical analyses")
    logger.info("=" * 60)
    
    difficulty_validation = validate_difficulty(results, problem_map)
    
    confidence_intervals = compute_bootstrap_ci(agreement_rates, n_per_style)
    
    mcnemar = compute_mcnemar_test(results)
    sign_test = compute_paired_sign_test(results)
    trend_test = compute_spearman_trend(results)
    
    divergence = compute_divergence(results)
    effect_sizes = compute_effect_sizes(mcnemar, sign_test, agreement_rates)
    stratified = stratified_analysis(results, problem_map)
    
    # Prepare aggregated metrics
    metrics_agg = {
        "total_results": len(results),
        "short_agreement_rate": agreement_rates.get("short", 0),
        "medium_agreement_rate": agreement_rates.get("medium", 0),
        "long_agreement_rate": agreement_rates.get("long", 0),
        "short_accuracy": divergence.get("short", {}).get("accuracy", 0),
        "medium_accuracy": divergence.get("medium", {}).get("accuracy", 0),
        "long_accuracy": divergence.get("long", {}).get("accuracy", 0),
        "mcnemar_p_value": mcnemar["p_value"],
        "sign_test_p_value": sign_test["p_value"],
        "spearman_r": trend_test["spearman_r"],
        "spearman_p_value": trend_test["p_value"],
        "cohens_h": effect_sizes["cohens_h_short_vs_long"],
        "divergence_short": divergence.get("short", {}).get("divergence", 0),
        "divergence_medium": divergence.get("medium", {}).get("divergence", 0),
        "divergence_long": divergence.get("long", {}).get("divergence", 0),
    }
    
    # Prepare dataset examples with eval metrics
    problem_results_map = defaultdict(dict)
    for r in results:
        problem_results_map[r["problem_index"]][r["cot_style"]] = r
    
    examples = []
    for idx, r in enumerate(results):
        # Get problem metadata
        if idx in problem_map:
            pm = problem_map[idx]
            input_text = f"Problem: {pm['input'][:200]}...\nCoT Style: {r['cot_style']}"
            output_text = f"Agreement: {r['agreement']}, COT Correct: {r['cot_correct']}, Self-Check Correct: {r['selfcheck_correct']}"
        else:
            input_text = f"Problem index: {r['problem_index']}, CoT Style: {r['cot_style']}"
            output_text = f"Agreement: {r['agreement']}, COT Correct: {r['cot_correct']}, Self-Check Correct: {r['selfcheck_correct']}"
        
        example = {
            "input": input_text,
            "output": output_text,
            "metadata_problem_index": str(r["problem_index"]),
            "metadata_cot_style": r["cot_style"],
            "metadata_agreement": str(r["agreement"]),
            "metadata_cot_correct": str(r["cot_correct"]),
            "metadata_selfcheck_correct": str(r["selfcheck_correct"]),
            "predict_agreement": "1" if r["agreement"] else "0",
            "predict_cot_correct": "1" if r["cot_correct"] else "0",
            "predict_selfcheck_correct": "1" if r["selfcheck_correct"] else "0",
            "eval_agreement_rate": round(agreement_rates.get(r["cot_style"], 0), 6),
            "eval_divergence": round(divergence.get(r["cot_style"], {}).get("divergence", 0), 6),
        }
        examples.append(example)
    
    datasets = [
        {
            "dataset": "openai/gsm8k",
            "examples": examples
        }
    ]
    
    # Build final output - conform to schema (no extra top-level keys)
    # Add statistical test results to metadata
    metadata = {
        "evaluation_name": "self_check_divergence_analysis",
        "description": "Statistical analysis of self-check divergence across CoT lengths",
        "hypothesis": "Shorter chain-of-thought reduces contradiction in model self-checks",
        "experiment_model": "mistralai/ministral-3b-2512",
        "temperature": 0.7,
        "bootstrap_iterations": BOOTSTRAP_ITERATIONS,
        "ci_level": CI_LEVEL,
        "difficulty_validation": difficulty_validation,
        "confidence_intervals": confidence_intervals,
        "mcnemar_test": mcnemar,
        "paired_sign_test": sign_test,
        "spearman_trend_test": trend_test,
        "divergence_analysis": divergence,
        "effect_sizes": effect_sizes,
        "difficulty_stratified": stratified,
    }
    
    output = {
        "metadata": metadata,
        "metrics_agg": metrics_agg,
        "datasets": datasets,
    }
    
    # Save output
    OUTPUT_FILE.write_text(json.dumps(output, indent=2))
    logger.info(f"Saved evaluation results to {OUTPUT_FILE}")
    
    # Log summary
    logger.info("=" * 60)
    logger.info("SUMMARY")
    logger.info("=" * 60)
    logger.info(f"Total results: {len(results)}")
    for style in ["short", "medium", "long"]:
        logger.info(f"{style}: agreement={agreement_rates.get(style, 0):.3f}, n={n_per_style.get(style, 0)}")
    logger.info(f"McNemar p-value: {mcnemar['p_value']:.6f}")
    logger.info(f"Spearman rho: {trend_test['spearman_r']:.4f}, p={trend_test['p_value']:.6f}")
    logger.info(f"Cohen's h: {effect_sizes['cohens_h_short_vs_long']:.4f} ({effect_sizes['interpretation']})")


if __name__ == "__main__":
    import sys
    # Force flush stdout
    sys.stdout.reconfigure(line_buffering=True)
    main()
