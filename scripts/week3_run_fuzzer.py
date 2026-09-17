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
