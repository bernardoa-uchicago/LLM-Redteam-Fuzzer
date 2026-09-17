"""
Week 4: full attack sweep across all seed behaviors x all strategies.

TODO:
- Load the full JBB-Behaviors set
- Run pipeline.run_sweep with all four strategies
- This will take a while against Groq's rate limits -- add a small
  sleep/backoff between calls if you hit 429s
- Output: results/week4_attempts.jsonl
"""
