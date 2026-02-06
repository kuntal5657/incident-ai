from openai import OpenAI
from app.config.settings import Settings

client = OpenAI(api_key=Settings.OPENAI_API_KEY)

job_id = "ftjob-KtPiTVULoDoij9yt1231mJvV"  # your job ID

# job_id = "ftjob-sHCUr3NtFtws8WuJ1iHsPs5h"

job = client.fine_tuning.jobs.retrieve(job_id)

print("Status:", job.status)

# 🔍 If failed, print the error clearly
if job.status == "failed":
    print("\n❌ Fine-tuning failed reason:")
    print(job.error)

# ✅ If succeeded, print model name
if job.status == "succeeded":
    print("\n✅ Fine-tuned model name:")
    print(job.fine_tuned_model)
