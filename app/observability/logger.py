"""
Structured JSON logger for observability.

This logger is:
- machine readable
- production friendly
- easy to ship to log systems later
"""

import json
import logging
import sys
from datetime import datetime

class JsonFormatter(logging.Formatter):
    STANDARD_ATTRS = {
        "name",
        "msg",
        "args",
        "levelname",
        "levelno",
        "pathname",
        "filename",
        "module",
        "exc_info",
        "exc_text",
        "stack_info",
        "lineno",
        "funcName",
        "created",
        "msecs",
        "relativeCreated",
        "thread",
        "threadName",
        "processName",
        "process",
    }

    def format(self, record: logging.LogRecord) -> str:
        log_record = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
            "logger": record.name,
        }

        # 🔑 Extract structured fields passed via `extra`
        for key, value in record.__dict__.items():
            if key not in self.STANDARD_ATTRS:
                log_record[key] = value

        return json.dumps(log_record)



def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)

    if logger.handlers:
        return logger  # already configured

    logger.setLevel(logging.INFO)

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JsonFormatter())

    logger.addHandler(handler)
    logger.propagate = False

    return logger
