"""
Week 5: replay Week 4's attempts through the guardrail and measure the drop
in attack success rate.

TODO:
- Load results/week4_attempts.jsonl
- For each attempt, run Guardrail.check_input on the prompt and/or
  check_output on the response
- Recompute ASR as if the guardrail had been in place all along
- Also run the guardrail against a sample of BENIGN JBB prompts to measure
  the false-positive rate -- a guardrail that blocks everything looks
  great on ASR alone and is useless in practice
- Output: results/week5_defense_eval.jsonl + summary stats
"""
