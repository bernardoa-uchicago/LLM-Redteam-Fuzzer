"""
Week 2: baseline attack surface, before your custom fuzzer exists.

Runs two off-the-shelf scanners against the target model and saves both
reports under results/baseline/. Neither tool goes through your target.py --
they talk to Ollama directly.

Requires `garak` and `promptfoo` installed on PATH (see README).
Run from the project root: python scripts/week2_baseline_scan.py
"""

import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from config import TARGET_MODEL

RESULTS_DIR = Path(__file__).parent.parent / "results" / "baseline"
GARAK_DIR = RESULTS_DIR / "garak"
PROMPTFOO_DIR = RESULTS_DIR / "promptfoo"
GARAK_DIR.mkdir(parents=True, exist_ok=True)
PROMPTFOO_DIR.mkdir(parents=True, exist_ok=True)

# A focused probe set rather than garak's full suite -- the full suite is
# large and this is a 3B model over local inference, so keep the first pass
# fast. Expand this list once you've confirmed the pipeline works end to end.
GARAK_PROBES = "dan,encoding,promptinject"


def run_garak():
    print("Running garak...")
    prefix = str(GARAK_DIR / "baseline")
    cmd = [
        "garak",
        "--model_type", "ollama",
        "--model_name", TARGET_MODEL,
        "--probes", GARAK_PROBES,
        "--report_prefix", prefix,
    ]
    subprocess.run(cmd, check=True)
    return Path(f"{prefix}.report.jsonl")


def summarize_garak(report_path: Path):
    if not report_path.exists():
        print(f"Warning: expected garak report at {report_path}, not found")
        return None

    total, hits = 0, 0
    with report_path.open() as f:
        for line in f:
            row = json.loads(line)
            if row.get("entry_type") == "eval":
                total += row.get("total", 0)
                hits += row.get("passed", 0)  # garak's "passed" = model resisted; hits below

    # garak's eval entries report attempts and how many the model successfully
    # defended against -- ASR is the inverse of the defended fraction
    if total == 0:
        return None
    defended = hits
    asr = 1 - (defended / total)
    print(f"Garak baseline: {total} attempts, ASR = {asr:.1%}")
    return {"tool": "garak", "total": total, "asr": asr}


def run_promptfoo():
    print("Running promptfoo redteam...")
    output_path = PROMPTFOO_DIR / "results.json"
    cmd = [
        "promptfoo", "redteam", "run",
        "-c", "promptfooconfig.yaml",
        "-o", str(output_path),
    ]
    # NOTE: verify this is still the right subcommand with `promptfoo redteam --help` --
    # promptfoo's CLI has changed shape across versions (generate+eval used to be
    # separate steps). If `redteam run` doesn't exist on your installed version,
    # fall back to `promptfoo redteam generate -o redteam-tests.yaml` followed by
    # `promptfoo eval -c redteam-tests.yaml -o <output_path>`.
    subprocess.run(cmd, check=True)
    return output_path


def summarize_promptfoo(output_path: Path):
    if not output_path.exists():
        print(f"Warning: expected promptfoo output at {output_path}, not found")
        return None

    with output_path.open() as f:
        data = json.load(f)

    results = data.get("results", {}).get("results", [])
    total = len(results)
    failed = sum(1 for r in results if not r.get("success", True))
    if total == 0:
        return None
    asr = failed / total
    print(f"Promptfoo baseline: {total} tests, ASR = {asr:.1%}")
    return {"tool": "promptfoo", "total": total, "asr": asr}


if __name__ == "__main__":
    garak_report = run_garak()
    garak_summary = summarize_garak(garak_report)

    promptfoo_output = run_promptfoo()
    promptfoo_summary = summarize_promptfoo(promptfoo_output)

    summary = {"garak": garak_summary, "promptfoo": promptfoo_summary}
    with (RESULTS_DIR / "baseline_summary.json").open("w") as f:
        json.dump(summary, f, indent=2)

    print(f"\nSaved combined summary to {RESULTS_DIR / 'baseline_summary.json'}")