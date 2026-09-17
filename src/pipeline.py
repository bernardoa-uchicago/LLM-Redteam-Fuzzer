"""
Top-level orchestrator. Wires together target/attacker/judge/defense and
one strategy, runs it across a list of seed behaviors, and logs every
attempt.

scripts/week3_run_fuzzer.py and scripts/week4_full_sweep.py both call into
this file -- implement it once, reuse it for the smoke test and the full
sweep.
"""


def run_behavior(behavior: dict, strategy: str, target, attacker, judge, logger, guardrail=None):
    """
    behavior: one row from JBB-Behaviors, e.g. {"id": ..., "goal": ..., "category": ...}
    strategy: "encoding" | "roleplay" | "crescendo" | "tap"
    guardrail: if provided, also check_input/check_output before/after
               hitting the target, and log whether it would have blocked
               this attempt

    TODO:
    - Dispatch to the right strategy module/class based on `strategy`
    - Run it, get back one or more attempt results
    - If `guardrail` is set, record whether it would have blocked the
      prompt and/or the response
    - Log every attempt via logger.log(...)
    """
    raise NotImplementedError


def run_sweep(behaviors: list, strategies: list, logger_path: str, guardrail=None):
    """
    TODO:
    - Loop over behaviors x strategies, call run_behavior for each
    - Show progress (tqdm)
    - Wrap each individual attempt in try/except and log failures --
      one bad response shouldn't kill a multi-hour sweep
    """
    raise NotImplementedError
