"""
Fine-tuning training script.

This script:
- Uploads training & eval datasets
- Creates a fine-tuning job
- Prints the resulting model name
"""

from openai import OpenAI
from app.config.settings import Settings

client = OpenAI(api_key=Settings.OPENAI_API_KEY)

# 1️⃣ Upload files
train_file = client.files.create(
    file=open("data/fine_tuning/train.jsonl", "rb"),
    purpose="fine-tune",
)

eval_file = client.files.create(
    file=open("data/fine_tuning/eval.jsonl", "rb"),
    purpose="fine-tune",
)

print("Train file ID:", train_file.id)
print("Eval file ID:", eval_file.id)

# 2️⃣ Create fine-tuning job
job = client.fine_tuning.jobs.create(
    model="gpt-3.5-turbo",
    training_file=train_file.id,
    validation_file=eval_file.id,
)

print("Fine-tuning job started:")
print("Job ID:", job.id)
