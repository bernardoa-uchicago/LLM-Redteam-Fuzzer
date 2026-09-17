"""
Role-play / persona-framing mutation strategy.

Idea: convince the target model it's writing fiction, playing a character,
or acting as an unrestricted alternate persona (the classic "DAN prompt"
family). Tests whether the target's refusal behavior is keyed too heavily
on surface-level context rather than the actual content being requested.
"""


def build_prompt(behavior: str, persona: str = "novelist") -> str:
    """
    TODO:
    - Write a framing template that wraps `behavior` inside a role-play or
      fictional scenario matching `persona`
    - Return the full prompt text

    Try a few personas (novelist writing a thriller, security researcher
    documenting an attack, actor rehearsing a script) and keep whichever
    ones show measurable success -- that becomes part of your taxonomy.
    """
    raise NotImplementedError
