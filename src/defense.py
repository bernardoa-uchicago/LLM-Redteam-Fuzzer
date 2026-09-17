"""
Guardrail layer: classifies whether a prompt (input-side, Prompt Guard 2) or
a response (output-side, GPT-OSS-Safeguard) should be blocked.

Used in Week 5 to re-run the Week 4 attack log through a defended pipeline
and measure the drop in attack success rate, plus the false-positive rate
on benign prompts.
"""

from groq import Groq
from config import GROQ_API_KEY, PROMPT_GUARD_MODEL, SAFEGUARD_MODEL


class Guardrail:
    def __init__(self):
        self.client = Groq(api_key=GROQ_API_KEY)

    def check_input(self, prompt: str) -> dict:
        """
        TODO: call PROMPT_GUARD_MODEL on `prompt`, return
        {"blocked": bool, "score": float}
        """
        raise NotImplementedError

    def check_output(self, behavior: str, response: str) -> dict:
        """
        TODO: call SAFEGUARD_MODEL with a written safety policy (define one
        in a docstring or a separate policy.md -- GPT-OSS-Safeguard is
        policy-following, not fixed-taxonomy), return
        {"blocked": bool, "category": str}
        """
        raise NotImplementedError
