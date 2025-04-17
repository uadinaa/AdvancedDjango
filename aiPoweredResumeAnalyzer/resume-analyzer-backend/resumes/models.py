from django.db import models
from django.conf import settings
from django.db import models


def resume_upload_path(instance, filename):
    return f"resumes/{instance.user.id}/{filename}"


class Resume(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    file = models.FileField(upload_to=resume_upload_path)  # Store the file itself
    filename = models.CharField(max_length=255, blank=True)  # Store the file name explicitly (optional)
    uploaded_at = models.DateTimeField(auto_now_add=True)  # Timestamp for when it was uploaded

    def save(self, *args, **kwargs):
        if not self.filename and self.file:
            self.filename = self.file.name
        super().save(*args, **kwargs)

    def __str__(self):
        return self.filename  # Display filename when you reference the model instance
