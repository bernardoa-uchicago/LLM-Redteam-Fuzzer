"""
Week 4: full attack sweep across all seed behaviors x all strategies.

TODO:
- Load the full JBB-Behaviors set
- Run pipeline.run_sweep with all four strategies
- This will take a while against Groq's rate limits -- add a small
  sleep/backoff between calls if you hit 429s
- Output: results/week4_attempts.jsonl
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
run_sweep(behaviors, ["encoding", "roleplay"], 
          "results/week4_full_sweep.jsonl", guardrail=None, encoding="base64", 
          persona="novelist")
run_sweep(behaviors, ["encoding", "roleplay"], 
          "results/week4_full_sweep.jsonl", guardrail=None, encoding="rot_13", 
          persona="novelist")
run_sweep(behaviors, ["encoding", "roleplay"], 
          "results/week4_full_sweep.jsonl", guardrail=None, encoding="base64", 
          persona="security_researcher")
run_sweep(behaviors, ["encoding", "roleplay"], 
          "results/week4_full_sweep.jsonl", guardrail=None, encoding="rot_13", 
          persona="security_researcher")
run_sweep(behaviors, ["encoding", "roleplay"], 
          "results/week4_full_sweep.jsonl", guardrail=None, encoding="base64", 
          persona="actor")
run_sweep(behaviors, ["encoding", "roleplay"], 
          "results/week4_full_sweep.jsonl", guardrail=None, encoding="rot_13", 
          persona="actor")