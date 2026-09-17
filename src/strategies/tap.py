"""
Tree-of-Attacks-with-Pruning (TAP).

Uses `attacker` as a candidate generator and `judge` as a scorer to do a
branching search over prompt variations: generate several candidates from
the current best node(s), score each against `target`, keep the most
promising branches, prune the rest, repeat until a success is found or
max depth is reached.

This is the most involved strategy -- implement encoding/roleplay/crescendo
first and come back to this one.
"""


class TAPStrategy:
    def __init__(self, behavior: str, branch_width: int, max_depth: int):
        self.behavior = behavior
        self.branch_width = branch_width
        self.max_depth = max_depth

    def run(self, attacker, target, judge) -> dict:
        """
        TODO:
        - Maintain a list of "nodes" (partial attack prompts + scores so far)
        - At each depth: expand each surviving node into `branch_width` new
          candidates via attacker.generate_candidate(..., strategy="tap")
        - Score each candidate's target response with judge.score(...)
        - Keep the top-N nodes by score, discard the rest (the "pruning")
        - Return the best result found, with the full search trace attached
          for logging
        """
        raise NotImplementedError
