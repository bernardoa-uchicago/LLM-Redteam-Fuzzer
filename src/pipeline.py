"""
Top-level orchestrator. Wires together target/attacker/judge/defense and
one strategy, runs it across a list of seed behaviors, and logs every
attempt.

scripts/week3_run_fuzzer.py and scripts/week4_full_sweep.py both call into
this file -- implement it once, reuse it for the smoke test and the full
sweep.
"""
from attacker import AttackerModel
from target import TargetModel
from judge import Judge
from logger import AttemptLogger
from strategies import encoding, roleplay, crescendo, tap
from config import MAX_CRESCENDO_TURNS, TAP_BRANCH_WIDTH, TAP_MAX_DEPTH, TARGET_MODEL, JUDGE_MODEL, ATTACKER_MODEL
from tqdm import tqdm

def run_behavior(behavior: dict, strategy: str, target, attacker, judge, logger, guardrail=None, **kwargs):
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
    behavior_success = None
    match strategy:
        case "encoding":
            prompt =encoding.build_prompt(behavior["goal"], encoding=kwargs.get("encoding", "base64"))
            resp = target.single_turn(prompt)
            score = judge.score(behavior["goal"], resp)
            logger.log(behavior_id=behavior["id"], strategy=strategy, turn=1,
						 prompt=prompt, response=resp, success=score["success"], 
                         category=behavior["category"], confidence= score["confidence"],
                         blocked_by_guardrail=None)
            return score["success"]
        case "roleplay":
            prompt =roleplay.build_prompt(behavior["goal"], persona=kwargs.get("persona", "novelist"))
            resp = target.single_turn(prompt)
            score = judge.score(behavior["goal"], resp)
            logger.log(behavior_id=behavior["id"], strategy=strategy, turn=1,
						 prompt=prompt, response=resp, success=score["success"],
                         confidence= score["confidence"], category=behavior["category"], 
                         blocked_by_guardrail=None)
            return score["success"]
        case "crescendo":
            strat = crescendo.CrescendoStrategy(behavior=behavior["goal"], max_turns=MAX_CRESCENDO_TURNS)
            while strat.turn < strat.max_turns:
                res = strat.next_turn(attacker, target, judge)
                logger.log(behavior_id=behavior["id"], strategy=strategy, turn=res["turn"],
					prompt=res["prompt"], response=res["response"], success=res["success"], 
                    confidence= res["confidence"],category=behavior["category"],
					blocked_by_guardrail=None)
                if res["success"]:
                    break
            return res["success"]
        case "tap":
            strat = tap.TAPStrategy(behavior=behavior["goal"], branch_width=TAP_BRANCH_WIDTH, max_depth=TAP_MAX_DEPTH)
            res = strat.run(attacker, target, judge)
            for depth, candidates in enumerate(res["trace"]):
                for node in candidates:
                    logger.log(behavior_id=behavior["id"], strategy=strategy, turn=depth, prompt=node["prompt"],
                               response=node["response"], success=node["success"], confidence=node["confidence"],
                               category=behavior["category"], blocked_by_guardrail=None)
            return res["best_scorer"]["success"]
        case _:
            raise ValueError(f"Unsupported strategy: {strategy}")


def run_sweep(behaviors: list, strategies: list, logger_path: str, guardrail=None, **kwargs):
    """
    TODO:
    - Loop over behaviors x strategies, call run_behavior for each
    - Show progress (tqdm)
    - Wrap each individual attempt in try/except and log failures --
      one bad response shouldn't kill a multi-hour sweep
    """
    target = TargetModel()
    attacker = AttackerModel()
    judge = Judge()
    logger = AttemptLogger(logger_path)
    for behavior in tqdm(behaviors, desc="Behaviors"):
        for strategy in strategies:
            try:
                run_behavior(behavior,strategy,target, attacker, judge, logger, **kwargs)
            except Exception as e:
                logger.log(behavior_id=behavior["id"], strategy=strategy, turn=-1,
             prompt=behavior["goal"], response="-1", success="-1",  confidence=None,
             category=behavior["category"], blocked_by_guardrail=None, error=str(e))
