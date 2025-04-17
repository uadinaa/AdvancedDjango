from celery import shared_task
import time

@shared_task
def process_resume(resume_id):
    # Simulate processing a resume (you could use AI parsing here)
    print(f"Processing resume {resume_id}...")
    time.sleep(5)  # Simulating a long task
    print(f"Resume {resume_id} processing complete!")
    return resume_id  # Could return parsed data or status
