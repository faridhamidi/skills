#!/usr/bin/env python3
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import sys


REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from evals.ptm_eval.case import Case
from evals.ptm_eval.runner import run_trial


def parse_args():
    parser = argparse.ArgumentParser(description="Run isolated PTM skill evaluations")
    parser.add_argument("--case", type=Path, required=True)
    parser.add_argument(
        "--condition",
        choices=("control", "treatment", "both"),
        default="both",
    )
    parser.add_argument("--trials", type=int, default=1)
    parser.add_argument("--model")
    parser.add_argument("--timeout", type=int, default=600)
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument(
        "--agent-command",
        help="Command template with optional {workspace}, {prompt}, and {condition} fields",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.trials <= 0:
        raise SystemExit("--trials must be positive")
    case_path = args.case if args.case.is_absolute() else REPO_ROOT / args.case
    case = Case.load(case_path, REPO_ROOT)
    output_dir = args.output_dir or (
        REPO_ROOT
        / "evals/results"
        / datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    )
    conditions = ("control", "treatment") if args.condition == "both" else (args.condition,)
    results = []
    for condition in conditions:
        for _ in range(args.trials):
            result = run_trial(
                case=case,
                condition=condition,
                output_dir=output_dir,
                repo_root=REPO_ROOT,
                command_template=args.agent_command,
                model=args.model,
                timeout=args.timeout,
            )
            results.append(result)
            summary = {
                "condition": condition,
                "result_dir": result["result_dir"],
                "agent_returncode": result["agent"]["returncode"],
                "project_tests": result["validation"]["project_tests"]["passed"],
                "hidden_oracle": result["validation"]["hidden_oracle"]["passed"],
                "intent_tags": result["validation"]["intent_tags"]["passed"],
            }
            print(json.dumps(summary, sort_keys=True), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
