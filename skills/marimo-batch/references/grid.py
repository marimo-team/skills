#!/usr/bin/env python3
# /// script
# dependencies = [
#     "huggingface-hub>=0.34",
#     "numpy",
#     "python-dotenv",
# ]
# ///
"""
Randomized hyperparameter grid launcher for starting-point.py.

This script samples random hyperparameter combinations and launches
each one as a separate job. By default it does a dry run so you can
inspect the combinations before committing to actual compute.

Usage:
    uv run grid.py                 # dry run, prints 12 combos
    uv run grid.py --count 20      # dry run, prints 20 combos
    uv run grid.py --launch        # actually submit jobs

Note on compute providers:
    This reference uses Hugging Face Jobs (via `huggingface_hub.run_uv_job`)
    as the compute backend, but this is just one option. You could swap it
    out for Modal, RunPod, or any other provider that can run a uv script.
    We use HF Jobs here because it provides a nice self-contained example.
"""

import argparse
import os
import random
import shlex
from pathlib import Path

import numpy as np
from dotenv import load_dotenv

# Hugging Face Jobs is just one compute provider — see the note in the
# module docstring above. Replace this with your provider of choice.
from huggingface_hub import run_uv_job


PROJECT_DIR = Path(__file__).resolve().parent
NOTEBOOK_PATH = PROJECT_DIR / "starting-point.py"

FLAVOR = "a100-large"
TIMEOUT = "6h"
JOB_ENV = {
    "PYTHONUNBUFFERED": "1",
    "PYTORCH_ALLOC_CONF": "expandable_segments:True",
}

# The search space keys must match the ModelParams fields in starting-point.py.
# Adjust the ranges and values to suit your experiment.
SEARCH_SPACE = {
    "epochs": [10, 15, 20, 25, 30, 40, 50],
    "batch_size": [8, 16, 32, 64, 128, 256, 512],
    "learning_rate": np.logspace(np.log10(1e-5), np.log10(5e-4), num=10).tolist(),
}

FIXED = {
    "wandb_project": "batch-sizes",
}


def normalize_value(value: object) -> object:
    if isinstance(value, np.integer):
        return int(value)
    if isinstance(value, np.floating):
        return float(value)
    return value


def format_value(value: object) -> str:
    value = normalize_value(value)
    if isinstance(value, float):
        return f"{value:.6g}"
    return str(value)


def build_run_name(params: dict[str, str]) -> str:
    return (
        f"e{params['epochs']}"
        f"-bs{params['batch_size']}"
        f"-lr{params['learning_rate']}"
    )


def sample_runs(count: int, rng: random.Random) -> list[dict[str, str]]:
    keys = list(SEARCH_SPACE.keys())
    seen: set[tuple[str, ...]] = set()
    runs: list[dict[str, str]] = []

    max_unique = 1
    for values in SEARCH_SPACE.values():
        max_unique *= len(values)

    target = min(count, max_unique)
    while len(runs) < target:
        params = {key: normalize_value(rng.choice(SEARCH_SPACE[key])) for key in keys}
        signature = tuple(format_value(params[key]) for key in keys)
        if signature in seen:
            continue
        seen.add(signature)

        run = {key: format_value(value) for key, value in params.items()}
        run.update(FIXED)
        run["wandb_run_name"] = build_run_name(run)
        runs.append(run)

    return runs


def params_to_cli_args(params: dict[str, str]) -> list[str]:
    args: list[str] = []
    for key, value in params.items():
        args.extend([f"--{key.replace('_', '-')}", str(value)])
    return args


def print_run(index: int, total: int, params: dict[str, str]) -> None:
    cli_args = params_to_cli_args(params)
    print(f"[{index}/{total}] {params['wandb_run_name']}")
    print(f"  flavor: {FLAVOR}")
    print(f"  timeout: {TIMEOUT}")
    print(f"  args: {' '.join(shlex.quote(arg) for arg in cli_args)}")


def load_secrets() -> dict[str, str]:
    load_dotenv(PROJECT_DIR / ".env")
    secrets: dict[str, str] = {}
    for key in ("HF_TOKEN", "WANDB_API_KEY"):
        value = os.environ.get(key)
        if not value:
            raise SystemExit(f"Missing required secret: {key}")
        secrets[key] = value
    return secrets


# This function uses huggingface_hub.run_uv_job to launch jobs.
# Swap this out if you use a different compute provider.
def launch_run(index: int, total: int, params: dict[str, str], secrets: dict[str, str]) -> None:
    print_run(index, total, params)
    job = run_uv_job(
        str(NOTEBOOK_PATH),
        script_args=params_to_cli_args(params),
        flavor=FLAVOR,
        timeout=TIMEOUT,
        env=JOB_ENV,
        secrets=secrets,
    )
    print(f"  launched: {job.url}")
    print()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Launch randomized hyperparameter sweeps for starting-point.py"
    )
    parser.add_argument(
        "--count",
        type=int,
        default=12,
        help="Number of randomized parameter combinations to sample.",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=0,
        help="RNG seed used to sample combinations.",
    )
    parser.add_argument(
        "--launch",
        action="store_true",
        help="Actually submit the sampled runs. Without this flag, only a dry run is printed.",
    )
    args = parser.parse_args()

    if args.count <= 0:
        raise SystemExit("--count must be positive")

    rng = random.Random(args.seed)
    runs = sample_runs(args.count, rng)
    secrets = load_secrets() if args.launch else None

    print(
        f"Randomized grid search with {len(runs)} runs "
        f"(requested={args.count}, seed={args.seed})"
    )
    print(f"Notebook: {NOTEBOOK_PATH.name}")
    print(f"Flavor: {FLAVOR}")
    print(f"Timeout: {TIMEOUT}")
    print(f"Fixed params: {FIXED}")
    print(f"Job env: {JOB_ENV}")
    print()

    for index, params in enumerate(runs, start=1):
        if args.launch:
            launch_run(index, len(runs), params, secrets)
        else:
            print_run(index, len(runs), params)
            print("  (dry run)")
            print()

    if not args.launch:
        print("Dry run complete. Pass --launch to submit jobs.")


if __name__ == "__main__":
    main()
