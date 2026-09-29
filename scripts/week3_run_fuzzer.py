"""
Week 3: smoke-test each custom strategy on a handful of seed behaviors
before running the full sweep.

TODO:
- Load 5-10 seed behaviors from data/jbb_behaviors.jsonl
- For each strategy in ["encoding", "roleplay", "crescendo", "tap"], call
  pipeline.run_sweep on just those seeds
- Manually inspect a few logged transcripts in results/ -- this is where
  you catch prompt-engineering bugs before scaling up
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src"))
print(sys.path)
from pipeline import run_sweep  # type: ignore
import json

behaviors = []
with open("data/jbb_behaviors.jsonl") as f:
    for line in f:
        behaviors.append(json.loads(line))
        if len(behaviors) == 10:
            break
run_sweep(behaviors, ["encoding", "roleplay", "crescendo", "tap"], 
          "results/week3_smoke.jsonl", guardrail=None, encoding="base64", 
          persona="novelist")