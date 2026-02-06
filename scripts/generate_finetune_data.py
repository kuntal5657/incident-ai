import json
import random

SYSTEM_PROMPT = (
    "You are an SRE incident classification system. "
    "Output ONLY valid JSON with fields: severity, category, "
    "probable_root_cause, recommended_actions, confidence."
)

SERVICES = [
    "orders-api",
    "payments-api",
    "catalog-api",
    "auth-service",
    "inventory-service",
]

INCIDENT_TEMPLATES = [
    {
        "title": "API latency spike",
        "description": "Latency increased after traffic surge",
        "category": "Performance",
        "root_cause": "Increased load causing downstream saturation",
        "actions": [
            "Investigate traffic patterns",
            "Add rate limiting",
            "Scale service horizontally",
        ],
        "severity": "P1",
        "confidence": (0.75, 0.9),
    },
    {
        "title": "Service error rate increase",
        "description": "5xx errors observed in production",
        "category": "Reliability",
        "root_cause": "Unhandled exceptions after recent deployment",
        "actions": [
            "Rollback recent deployment",
            "Inspect error logs",
            "Add missing exception handling",
        ],
        "severity": "P1",
        "confidence": (0.7, 0.85),
    },
    {
        "title": "Cache miss rate increase",
        "description": "Cache hit ratio dropped but service remains available",
        "category": "Performance",
        "root_cause": "Cache eviction under increased memory pressure",
        "actions": [
            "Review cache eviction policy",
            "Increase cache capacity",
            "Monitor backend latency",
        ],
        "severity": "P2",
        "confidence": (0.6, 0.75),
    },
    {
        "title": "Background job delay",
        "description": "Async jobs processing slower than expected",
        "category": "Throughput",
        "root_cause": "Worker pool saturation",
        "actions": [
            "Scale worker nodes",
            "Increase queue concurrency",
            "Review job retry logic",
        ],
        "severity": "P2",
        "confidence": (0.6, 0.8),
    },
]

def make_example():
    tpl = random.choice(INCIDENT_TEMPLATES)
    service = random.choice(SERVICES)

    user_prompt = (
        f"Incident:\n"
        f"Title: {tpl['title']}\n"
        f"Service: {service}\n"
        f"Environment: prod\n"
        f"Description: {tpl['description']}\n\n"
        f"Relevant Historical Context:\n"
        f"Similar incidents observed in the past."
    )

    assistant_json = {
        "severity": tpl["severity"],
        "category": tpl["category"],
        "probable_root_cause": tpl["root_cause"],
        "recommended_actions": tpl["actions"],
        "confidence": round(random.uniform(*tpl["confidence"]), 2),
    }

    return {
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
            {"role": "assistant", "content": json.dumps(assistant_json)},
        ]
    }

def write_jsonl(path, count):
    with open(path, "w", encoding="utf-8") as f:
        for _ in range(count):
            f.write(json.dumps(make_example()) + "\n")

if __name__ == "__main__":
    write_jsonl("data/fine_tuning/train.jsonl", 10)
    write_jsonl("data/fine_tuning/eval.jsonl", 5)
    print("✅ Generated 10 train and 5 eval examples")