from django.db import models

class Rating(models.Model):
    resume_file = models.FileField(upload_to='resumes/')
    final_score = models.FloatField()
    skill_gaps = models.TextField()
    formatting = models.TextField()
    ats_keywords = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)