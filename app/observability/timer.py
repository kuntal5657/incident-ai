import time
from app.observability.metrics import metrics


class Timer:
    def __init__(self, metric_name: str):
        self.metric_name = metric_name

    def __enter__(self):
        self.start = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc, tb):
        duration_ms = (time.perf_counter() - self.start) * 1000
        metrics.observe(self.metric_name, duration_ms)
