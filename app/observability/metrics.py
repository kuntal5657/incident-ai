"""
In-process metrics registry.

This is intentionally simple:
- no external dependencies
- easy to replace with Prometheus later
"""

import time
from collections import defaultdict


class MetricsRegistry:
    def __init__(self):
        self.counters = defaultdict(int)
        self.timings = defaultdict(list)

    # ---- Counters ----
    def inc(self, name: str, value: int = 1):
        self.counters[name] += value

    # ---- Timings ----
    def observe(self, name: str, duration_ms: float):
        self.timings[name].append(duration_ms)

    # ---- Snapshot (for logging / debugging) ----
    def snapshot(self):
        return {
            "counters": dict(self.counters),
            "timings": {
                k: {
                    "count": len(v),
                    "avg_ms": round(sum(v) / len(v), 2) if v else 0,
                    "max_ms": round(max(v), 2) if v else 0,
                }
                for k, v in self.timings.items()
            },
        }
    
    # ---- Cost tracking ----
    def add_tokens(self, prompt_tokens: int, completion_tokens: int):
        self.inc("llm.tokens.prompt", prompt_tokens)
        self.inc("llm.tokens.completion", completion_tokens)
        self.inc("llm.tokens.total", prompt_tokens + completion_tokens)

    def add_cost(self, cost_usd: float):
        self.inc("llm.cost.usd", round(cost_usd, 6))


# Global singleton (good enough for now)
metrics = MetricsRegistry()
