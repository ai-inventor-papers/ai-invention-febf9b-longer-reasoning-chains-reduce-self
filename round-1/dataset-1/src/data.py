#!/usr/bin/env python3
"""Prepare GSM8K dataset with difficulty tiers for self-check divergence experiment."""

from loguru import logger
from pathlib import Path
import json
import re
import random
import math
import sys

logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
logger.add("logs/run.log", rotation="30 MB", level="DEBUG")

random.seed(42)

WORKSPACE = Path("/ai-inventor/aii_data/runs/run_DyrN7YJjJoEX/3_invention_loop/iter_1/gen_art/gen_art_dataset_1")
TEMP_DIR = WORKSPACE / "temp" / "datasets"
OUTPUT_DIR = WORKSPACE / "data" / "gsm8k"


def extract_answer(answer_text: str) -> str:
    """Extract final numeric answer from GSM8K solution text (#### X format)."""
    match = re.search(r'####\s*(.+?)\s*$', answer_text, re.DOTALL)
    if match:
        return match.group(1).strip()
    # Fallback: last <<...>> pattern
    matches = re.findall(r'<<([^>>]+)>>', answer_text)
    if matches:
        return matches[-1].strip()
    return ""


def count_operations(text: str) -> int:
    """Count arithmetic operations in solution text."""
    ops = re.findall(r'[\+\-\*/]', text)
    return len(ops)


def count_numerics(text: str) -> int:
    """Count distinct numeric values in solution text."""
    numbers = re.findall(r'\b\d+\.?\d*\b', text)
    return len(set(numbers))


def count_sentences(text: str) -> int:
    """Count sentences in solution text."""
    sentences = re.split(r'[.!?]+', text)
    return len([s for s in sentences if s.strip()])


def count_tokens(text: str) -> int:
    """Count words in question text."""
    return len(text.split())


def count_multi_step_indicators(text: str) -> int:
    """Count multi-step reasoning indicators."""
    indicators = ['then', 'if', 'total', 'remaining', 'each', 'per', 'next', 'after', 'finally', 'first']
    text_lower = text.lower()
    return sum(1 for ind in indicators if ind in text_lower)


def compute_difficulty_score(question: str, answer: str) -> dict:
    """Compute difficulty score and features for a problem."""
    op_count = count_operations(answer)
    numeric_count = count_numerics(answer)
    sentence_count = count_sentences(answer)
    token_count = count_tokens(question)
    multi_step = count_multi_step_indicators(question + " " + answer)

    return {
        "operation_count": op_count,
        "numeric_count": numeric_count,
        "sentence_count": sentence_count,
        "token_count": token_count,
        "multi_step_indicators": multi_step,
    }


def normalize_scores(features_list: list) -> list:
    """Normalize all feature scores to [0, 1] range."""
    if not features_list:
        return []

    keys = ["operation_count", "numeric_count", "sentence_count", "token_count", "multi_step_indicators"]
    normalized = []

    for features in features_list:
        norm = {}
        for key in keys:
            vals = [f[key] for f in features_list]
            min_val, max_val = min(vals), max(vals)
            if max_val > min_val:
                norm[key] = (features[key] - min_val) / (max_val - min_val)
            else:
                norm[key] = 0.0
        normalized.append(norm)

    return normalized


def compute_final_score(norm: dict) -> float:
    """Compute weighted difficulty score."""
    score = (
        0.30 * norm["operation_count"]
        + 0.25 * norm["numeric_count"]
        + 0.20 * norm["sentence_count"]
        + 0.15 * norm["token_count"]
        + 0.10 * norm["multi_step_indicators"]
    )
    return round(score, 4)


def assign_tiers_quantile(processed: list) -> None:
    """Assign difficulty tiers using quantile-based binning for balanced distribution."""
    sorted_problems = sorted(processed, key=lambda p: p["difficulty_score"])
    n = len(sorted_problems)
    third = n // 3

    for i, p in enumerate(sorted_problems):
        if i < third:
            p["difficulty_tier"] = "easy"
        elif i < 2 * third:
            p["difficulty_tier"] = "medium"
        else:
            p["difficulty_tier"] = "hard"


@logger.catch(reraise=True)
def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Load GSM8K test and train splits
    test_path = TEMP_DIR / "full_openai_gsm8k_main_test.json"
    train_path = TEMP_DIR / "full_openai_gsm8k_main_train.json"

    all_problems = []
    for split_name, path in [("test", test_path), ("train", train_path)]:
        if not path.exists():
            logger.warning(f"Split not found: {path}")
            continue
        data = json.loads(path.read_text())
        for item in data:
            item["_split"] = split_name
            all_problems.append(item)

    logger.info(f"Loaded {len(all_problems)} total problems")

    # Extract answers and compute features
    processed = []
    skipped = 0
    for item in all_problems:
        question = item.get("question", "")
        answer_text = item.get("answer", "")
        ground_truth = extract_answer(answer_text)

        if not ground_truth:
            skipped += 1
            continue

        features = compute_difficulty_score(question, answer_text)
        processed.append({
            "question": question,
            "answer_text": answer_text,
            "ground_truth": ground_truth,
            "features": features,
            "split": item["_split"],
        })

    logger.info(f"Processed {len(processed)} problems (skipped {skipped})")

    # Normalize and score
    norm_features = normalize_scores([p["features"] for p in processed])
    for i, p in enumerate(processed):
        p["norm_features"] = norm_features[i]
        p["difficulty_score"] = compute_final_score(norm_features[i])

    # Assign tiers using quantile-based binning for balanced distribution
    assign_tiers_quantile(processed)

    # Count tiers
    tier_counts = {"easy": 0, "medium": 0, "hard": 0}
    for p in processed:
        tier_counts[p["difficulty_tier"]] += 1
    logger.info(f"Tier distribution: {tier_counts}")

    # Build examples for exp_sel_data_out schema
    examples = []
    for idx, p in enumerate(processed):
        example = {
            "input": p["question"],
            "output": p["ground_truth"],
            "metadata_difficulty_tier": p["difficulty_tier"],
            "metadata_difficulty_score": p["difficulty_score"],
            "metadata_solution_steps": p["answer_text"],
            "metadata_operation_count": p["features"]["operation_count"],
            "metadata_numeric_count": p["features"]["numeric_count"],
            "metadata_sentence_count": p["features"]["sentence_count"],
            "metadata_token_count": p["features"]["token_count"],
            "metadata_multi_step_indicators": p["features"]["multi_step_indicators"],
            "metadata_split": p["split"],
            "metadata_row_index": idx,
        }
        examples.append(example)

    # Build output structure
    output = {
        "metadata": {
            "source": "openai/gsm8k",
            "description": "GSM8K math word problems with difficulty stratification for self-check divergence experiment",
            "total_problems": len(examples),
            "tier_distribution": tier_counts,
            "difficulty_method": "heuristic scoring (operations, numerics, sentences, tokens, multi-step indicators)",
            "paper": "Cobbe et al. 2021 - Training Verifiers to Solve Math Word Problems",
        },
        "datasets": [
            {
                "dataset": "gsm8k",
                "examples": examples,
            }
        ],
    }

    # Save full dataset
    full_path = OUTPUT_DIR / "full_gsm8k.json"
    full_path.write_text(json.dumps(output, indent=2))
    logger.info(f"Saved full dataset: {full_path} ({len(examples)} examples)")

    # Create mini (50 problems, balanced tiers)
    tier_groups = {"easy": [], "medium": [], "hard": []}
    for ex in examples:
        tier = ex["metadata_difficulty_tier"]
        tier_groups[tier].append(ex)

    mini_examples = []
    per_tier = 17  # ~50 total
    for tier in ["easy", "medium", "hard"]:
        sampled = random.sample(tier_groups[tier], min(per_tier, len(tier_groups[tier])))
        mini_examples.extend(sampled)
    random.shuffle(mini_examples)

    mini_output = {
        "metadata": output["metadata"],
        "datasets": [{"dataset": "gsm8k", "examples": mini_examples}],
    }
    mini_path = OUTPUT_DIR / "mini_gsm8k.json"
    mini_path.write_text(json.dumps(mini_output, indent=2))
    logger.info(f"Saved mini dataset: {mini_path} ({len(mini_examples)} examples)")

    # Create preview (5 problems: 2 easy, 2 medium, 1 hard)
    preview_examples = []
    for tier, count in [("easy", 2), ("medium", 2), ("hard", 1)]:
        sampled = random.sample(tier_groups[tier], min(count, len(tier_groups[tier])))
        preview_examples.extend(sampled)

    # Truncate strings for preview
    def truncate(obj, max_len=200):
        if isinstance(obj, str):
            return obj[:max_len] + "..." if len(obj) > max_len else obj
        elif isinstance(obj, dict):
            return {k: truncate(v, max_len) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [truncate(item, max_len) for item in obj]
        return obj

    preview_output = truncate({
        "metadata": output["metadata"],
        "datasets": [{"dataset": "gsm8k", "examples": preview_examples}],
    })
    preview_path = OUTPUT_DIR / "preview_gsm8k.json"
    preview_path.write_text(json.dumps(preview_output, indent=2))
    logger.info(f"Saved preview dataset: {preview_path} ({len(preview_examples)} examples)")

    # Save summary
    summary = {
        "total_problems": len(examples),
        "tier_distribution": tier_counts,
        "difficulty_score_range": {
            "min": min(p["difficulty_score"] for p in processed),
            "max": max(p["difficulty_score"] for p in processed),
            "mean": sum(p["difficulty_score"] for p in processed) / len(processed),
        },
        "split_distribution": {
            "train": sum(1 for p in processed if p["split"] == "train"),
            "test": sum(1 for p in processed if p["split"] == "test"),
        },
        "files": {
            "full": str(full_path),
            "mini": str(mini_path),
            "preview": str(preview_path),
        },
    }
    summary_path = OUTPUT_DIR / "dataset_summary.json"
    summary_path.write_text(json.dumps(summary, indent=2))
    logger.info(f"Saved summary: {summary_path}")
    logger.info("Dataset preparation complete!")


if __name__ == "__main__":
    main()
