# LLM Jailbreak Fuzzer + Defense Evaluation

Automated red-teaming pipeline for a local open-weight LLM: discover jailbreak
patterns, categorize them, then build and measure a guardrail defense.

## Architecture

- **Target model** (the system under test): runs locally via Ollama on your
  machine. Small quantized model so it fits in 8GB of RAM.
- **Attacker + Judge** (generate attack candidates, score success): hosted on
  Groq's free API tier.
- **Defense/guardrail**: also hosted on Groq (Llama Prompt Guard 2 for
  input-side detection, GPT-OSS-Safeguard-20B for output-side classification).

## Setup

1. Install Ollama: https://ollama.com/download
2. Pull the target model:
   ```
   ollama pull llama3.2:3b-instruct-q4_K_M
   ```
3. Create a free Groq account and API key: https://console.groq.com
4. `cp .env.example .env` and paste in your `GROQ_API_KEY`
5. `pip install -r requirements.txt`
6. Download JailbreakBench's JBB-Behaviors dataset into `data/` (see
   `data/README.md`)
7. Run `python scripts/week1_setup_check.py` to confirm everything's wired up

## Project structure

```
config.py                    -- all model names, params, paths in one place
src/
  target.py                  -- wrapper for the local Ollama target model
  attacker.py                -- wrapper for the Groq-hosted attacker model
  judge.py                   -- wrapper for the Groq-hosted judge/scorer
  defense.py                 -- wrapper for the Groq-hosted guardrail models
  logger.py                  -- structured JSONL logging of every attempt
  pipeline.py                -- orchestrates target+attacker+judge+strategy
  strategies/
    encoding.py               -- base64/cipher obfuscation mutation
    roleplay.py               -- persona/fiction-framing mutation
    crescendo.py              -- multi-turn escalation strategy
    tap.py                    -- tree-of-attacks-with-pruning search
scripts/
  week1_setup_check.py        -- sanity-check every component
  week2_baseline_scan.py       -- Garak + Promptfoo baseline scan
  week3_run_fuzzer.py          -- smoke-test each strategy on a few seeds
  week4_full_sweep.py          -- full attack sweep, all behaviors x strategies
  week5_defense_eval.py        -- replay attempts through the guardrail
  week6_report.py              -- compute metrics, generate plots for writeup
data/                         -- JBB-Behaviors dataset goes here
results/                      -- all logs, reports, plots land here
tests/                        -- unit tests for strategies/judge logic
```

## How to work through this

Every file under `src/` and `scripts/` is a stub: docstrings and function
signatures are filled in, the actual logic is left as `TODO` /
`raise NotImplementedError`. Implement one file at a time, roughly in the
order: config.py -> target.py -> attacker.py -> judge.py -> one strategy
(start with encoding.py, it's the simplest) -> pipeline.py -> the week
scripts in order.

## References

- JailbreakBench: https://github.com/JailbreakBench/jailbreakbench
- PyRIT (for inspiration on the attacker/judge loop design):
  https://github.com/Azure/PyRIT
- Garak: https://github.com/leondz/garak
- Promptfoo: https://github.com/promptfoo/promptfoo
- Groq models/docs: https://console.groq.com/docs/models
