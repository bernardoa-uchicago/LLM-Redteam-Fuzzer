"""
Central configuration for the LLM red-team fuzzer project.

Fill in / adjust values as you set up each component. Nothing here should
contain secrets -- the Groq API key goes in .env, loaded via python-dotenv.
"""

import os
from dotenv import load_dotenv

load_dotenv()

# --- Target model (runs locally via Ollama) ---
OLLAMA_HOST = "http://localhost:11434"
TARGET_MODEL = "llama3.2:3b-instruct-q4_K_M"  # TODO: confirm exact tag after `ollama pull`

# --- Hosted models (via Groq API) ---
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
ATTACKER_MODEL = "openai/gpt-oss-20b"                      # generates/mutates attack prompts
JUDGE_MODEL = "openai/gpt-oss-120b"                          # scores whether an attempt succeeded
PROMPT_GUARD_MODEL = "meta-llama/llama-prompt-guard-2-86m"    # input-side jailbreak detector
SAFEGUARD_MODEL = "openai/gpt-oss-safeguard-20b"              # output-side policy classifier

# --- Experiment parameters ---
MAX_CRESCENDO_TURNS = 10       # TODO: tune based on what you observe
TAP_BRANCH_WIDTH = 3           # candidates generated per node
TAP_MAX_DEPTH = 5
TEMPERATURE_ATTACKER = 1.0     # higher = more diverse mutation attempts
TEMPERATURE_TARGET = 0.7
TEMPERATURE_JUDGE = 0.0        # want consistent grading, not creativity

# --- Paths ---
DATA_DIR = "data"
RESULTS_DIR = "results"
SEED_BEHAVIORS_FILE = f"{DATA_DIR}/jbb_behaviors.jsonl"
