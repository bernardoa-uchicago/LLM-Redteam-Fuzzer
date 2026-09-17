"""
Week 1 setup check: run this before writing any of the fuzzer logic to
confirm every external dependency actually works.

Checks:
1. Ollama is running and the target model responds to a trivial prompt
2. GROQ_API_KEY is set and a simple completion call succeeds
3. data/jbb_behaviors.jsonl and data/jbb_behaviors_benign.jsonl exist and
   have rows in them

Run from the project root:
    python scripts/week1_setup_check.py
"""

import json
import sys
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).parent.parent))
from config import (
    OLLAMA_HOST,
    TARGET_MODEL,
    GROQ_API_KEY,
    ATTACKER_MODEL,
    SEED_BEHAVIORS_FILE,
)

DATA_DIR = Path(__file__).parent.parent / "data"

results = []


def check(name):
    """Decorator-free helper: wraps a check function, records PASS/FAIL, never raises."""
    def wrapper(fn):
        try:
            detail = fn()
            results.append((name, True, detail or "ok"))
        except Exception as e:
            results.append((name, False, str(e)))
    return wrapper


def check_ollama_running():
    resp = requests.get(f"{OLLAMA_HOST}/api/tags", timeout=5)
    resp.raise_for_status()
    models = [m["name"] for m in resp.json().get("models", [])]
    if TARGET_MODEL not in models:
        raise RuntimeError(
            f"Ollama is running but {TARGET_MODEL!r} isn't pulled yet. "
            f"Available: {models}. Run: ollama pull {TARGET_MODEL}"
        )
    return f"{TARGET_MODEL} is available"


check("Ollama running + target model pulled")(check_ollama_running)


def check_target_responds():
    resp = requests.post(
        f"{OLLAMA_HOST}/api/chat",
        json={
            "model": TARGET_MODEL,
            "messages": [{"role": "user", "content": "Reply with the single word: pong"}],
            "stream": False,
        },
        timeout=30,
    )
    resp.raise_for_status()
    content = resp.json()["message"]["content"]
    if not content.strip():
        raise RuntimeError("Target model returned an empty response")
    return f"target replied: {content.strip()[:50]!r}"


check("Target model responds to a prompt")(check_target_responds)


def check_groq_key_set():
    if not GROQ_API_KEY:
        raise RuntimeError("GROQ_API_KEY is not set -- check your .env file")
    return "GROQ_API_KEY is set"


check("GROQ_API_KEY is set")(check_groq_key_set)


def check_groq_call_succeeds():
    from groq import Groq

    client = Groq(api_key=GROQ_API_KEY)
    completion = client.chat.completions.create(
        model=ATTACKER_MODEL,
        messages=[{"role": "user", "content": "Reply with the single word: pong"}],
        max_completion_tokens=200,   # gpt-oss needs headroom for reasoning tokens, not max_tokens=10
        reasoning_effort="low",      # keep it minimal for a trivial sanity check
        include_reasoning=False,     # only return the final answer, not the thinking trace
    )
    content = completion.choices[0].message.content
    if not content.strip():
        raise RuntimeError("Groq call succeeded but returned an empty response")
    return f"Groq replied: {content.strip()[:50]!r}"


check("Groq API call succeeds")(check_groq_call_succeeds)


def check_seed_data():
    path = Path(SEED_BEHAVIORS_FILE)
    if not path.exists():
        raise RuntimeError(f"{path} not found -- run your data conversion script first")
    with path.open() as f:
        rows = [json.loads(line) for line in f if line.strip()]
    if not rows:
        raise RuntimeError(f"{path} exists but has 0 rows")
    missing_keys = [k for k in ("id", "goal", "category") if k not in rows[0]]
    if missing_keys:
        raise RuntimeError(f"Rows are missing expected keys: {missing_keys}")
    return f"{len(rows)} seed behaviors loaded"


check("Seed behaviors dataset (jbb_behaviors.jsonl)")(check_seed_data)


def check_benign_data():
    path = DATA_DIR / "jbb_behaviors_benign.jsonl"
    if not path.exists():
        raise RuntimeError(f"{path} not found -- needed later for Week 5 false-positive testing")
    with path.open() as f:
        rows = [json.loads(line) for line in f if line.strip()]
    if not rows:
        raise RuntimeError(f"{path} exists but has 0 rows")
    return f"{len(rows)} benign behaviors loaded"


check("Benign behaviors dataset (jbb_behaviors_benign.jsonl)")(check_benign_data)


# --- Summary ---
print("\nWeek 1 Setup Check\n" + "=" * 40)
all_passed = True
for name, passed, detail in results:
    status = "PASS" if passed else "FAIL"
    if not passed:
        all_passed = False
    print(f"[{status}] {name}")
    print(f"       {detail}")

print("=" * 40)
print("All checks passed -- ready for Week 2." if all_passed else "Fix the FAILs above before moving on.")
sys.exit(0 if all_passed else 1)