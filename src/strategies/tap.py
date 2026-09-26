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
        self.nodes = []
        self.trace = []

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
        seed = {"prompt": self.behavior, "response": None, "confidence": None, "success": None}
        self.nodes.append(seed)
        self.trace.append([seed])
        for depth in range(self.max_depth):
            candidates = []
            for node in self.nodes:
                if node["response"] == None:
                    prompt = attacker.generate_candidate(node["prompt"], "tap")
                else:
                    prompt = attacker.generate_candidate(self.behavior, "tap", [{"prompt": node["prompt"], "response": node["response"]}])
                response = target.single_turn(prompt)
                results = judge.score(self.behavior, response)
                candidate = {"prompt": prompt, "response": response, "confidence": results["confidence"], "success": results["success"]}
                if candidate["success"]:
                    return {"best_scorer": candidate, "trace": self.trace}
                candidates.append(candidate)
            self.nodes += candidates
            self.trace.append(candidates)
            self.nodes = sorted(self.nodes, key=lambda x: x["confidence"], reverse=True)[:self.branch_width]
        return {"best_scorer": self.nodes[0], "trace": self.trace}
