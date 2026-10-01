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
import sys, os
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src"))
print(sys.path)
from defense import Guardrail
from target import TargetModel
import json
import time
from groq import RateLimitError

success = 0
total = 0
blocks_input = 0
blocks_output = 0
blocks_both = 0
false_positives_input = 0
false_positives_output = 0
benign_total = 0
target = TargetModel()
client = Guardrail()
with open("results/week5_guardrail.jsonl", "a") as log:
    with open("results/week4_attempts.jsonl") as f:
        for line in f:
            line = json.loads(line)
            if line["success"] != "-1":
                total += 1
                if line["success"]:
                    success += 1
                while True:
                    try:
                        input_score = client.check_input(line["prompt"])
                        output_score = client.check_output(line["behavior_id"], line["response"])
                        break
                    except RateLimitError as e:
                        wait_time = int(e.response.headers.get("retry-after", 60))
                        print(f"Rate limit hit, waiting {wait_time} seconds...")
                        time.sleep(wait_time)
                    except Exception as e:
                        print(f"Error: {e}")
                        input_score = {"blocked": None, "score": None}
                        output_score = {"blocked": None, "category": None}
                        break
                if input_score["blocked"] and output_score["blocked"] and line["success"]:
                    blocks_both += 1
                elif input_score["blocked"] and line["success"]:
                    blocks_input += 1
                elif output_score["blocked"] and line["success"]:
                    blocks_output += 1
                entry = {
                    **line,
                    "input_blocked": input_score["blocked"],
                    "input_score": input_score["score"],
                    "output_blocked": output_score["blocked"],
                    "output_category": output_score["category"]
                }
            else:
                entry = {
                        **line,
                        "input_blocked": None,
                        "input_score": None,
                        "output_blocked": None,
                        "output_category": None
                    }
            json.dump(entry, log)
            log.write("\n")

    with open("data/jbb_behaviors_benign.jsonl") as f:
        for line in f:
            line = json.loads(line)
            benign_total += 1
            response = target.single_turn(line["goal"])
            while True:
                try:
                    input_score = client.check_input(line["goal"])
                    output_score = client.check_output(line["id"], response)
                    break
                except RateLimitError as e:
                    wait_time = int(e.response.headers.get("retry-after", 60))
                    print(f"Rate limit hit, waiting {wait_time} seconds...")
                    time.sleep(wait_time)
                except Exception as e:
                    print(f"Error: {e}")
                    input_score = {"blocked": None, "score": None}
                    output_score = {"blocked": None, "category": None}
                    break
            if input_score["blocked"]:
                false_positives_input += 1
            if output_score["blocked"]:
                false_positives_output += 1

    summary = {
        "type": "summary",
        "total_attempts": total,
        "successful_attacks": success,
        "undefended_asr": success / total if total > 0 else 0,
        "blocks_input_only": blocks_input,
        "blocks_output_only": blocks_output,
        "blocks_both": blocks_both,
        "defended_asr": (success - blocks_input - blocks_output - blocks_both) / total if total > 0 else 0,
        "false_positive_rate_input": false_positives_input / benign_total if benign_total > 0 else 0,
        "false_positive_rate_output": false_positives_output / benign_total if benign_total > 0 else 0
    }
    json.dump(summary, log)
    log.write("\n")