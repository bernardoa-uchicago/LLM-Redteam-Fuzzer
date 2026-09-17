"""
Multi-turn escalation ("crescendo") strategy.

Starts fully benign and nudges the conversation toward the harmful behavior
over several turns, so no single message looks like a violation in
isolation. Stateful -- needs to track conversation history across calls.
"""


class CrescendoStrategy:
    def __init__(self, behavior: str, max_turns: int):
        self.behavior = behavior
        self.max_turns = max_turns
        self.history = []

    def next_turn(self, attacker, target, judge) -> dict:
        """
        One step of the escalation loop:
        1. Ask `attacker` for the next turn's prompt, given self.history and
           how many turns remain until self.max_turns
        2. Send it to `target`, append both prompt and response to
           self.history
        3. Ask `judge` whether the behavior has now been achieved
        4. Return {"turn": n, "prompt": ..., "response": ..., "success": bool}

        TODO: implement, stop early if the judge reports success or
        self.max_turns is reached
        """
        raise NotImplementedError
