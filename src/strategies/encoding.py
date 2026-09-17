"""
Encoding-based mutation strategy.

Idea: wrap the harmful behavior in an encoded form (base64, ROT13, or a
made-up substitution cipher) and ask the target model to decode and comply.
Tests whether the target's safety training generalizes past surface-level
keyword matching -- a model can be happy to decode a base64 string and
follow the instructions inside it, even though it would refuse the same
instructions in plain text.

This is the simplest strategy -- start here.
"""


def build_prompt(behavior: str, encoding: str = "base64") -> str:
    """
    TODO:
    - Encode `behavior` using the chosen scheme (base64, rot13, or a custom
      cipher you define)
    - Wrap it in an instruction telling the target model to decode the
      string and follow the instructions inside it
    - Return the full prompt text as a single string
    """
    raise NotImplementedError
