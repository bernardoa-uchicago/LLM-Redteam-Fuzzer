"""
Structured logging for every attack attempt. One JSON object per line
(JSONL), so scripts/week6_report.py can load the whole thing with
pandas.read_json(..., lines=True).

Keep the schema below stable once you start Week 4 -- changing field names
partway through a full sweep makes the report script painful to write.
"""

from pathlib import Path
import json
from datetime import datetime

class AttemptLogger:
    def __init__(self, path: str):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def log(self, *, behavior_id: str, strategy: str, turn: int,
             prompt: str, response: str, success: bool, category: str,
             blocked_by_guardrail: bool = None):
        """
        TODO: append one JSON object per line with all fields above plus a
        timestamp. Use "a" mode so repeated runs append rather than
        overwrite.
        """
        entry = {
            "behavior_id": behavior_id,
            "strategy": strategy,
            "turn": turn,
            "prompt": prompt,
            "response": response,
            "success": success,
            "category": category,
            "blocked_by_guardrail": blocked_by_guardrail,
            "time": datetime.now().isoformat()
        }
        with open(self.path, "a") as log:
            json.dump(entry, log)
            log.write("\n")
        return
