# Data

Download JailbreakBench's JBB-Behaviors dataset here as `jbb_behaviors.jsonl`
(one JSON object per line with at least `id`, `goal`, `category`, and whether
the behavior is harmful or benign).

Reference: https://github.com/JailbreakBench/jailbreakbench

You can either `pip install jailbreakbench` and export their dataset to this
format, or pull the raw CSV/JSON from their GitHub repo directly and
reshape it with a small script -- your call.
