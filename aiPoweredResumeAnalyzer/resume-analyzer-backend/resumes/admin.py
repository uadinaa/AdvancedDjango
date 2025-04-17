from django.contrib import admin
from .models import Resume


@admin.register(Resume)
class ResumeUploadAdmin(admin.ModelAdmin):
    list_display = ("user", "uploaded_at", "filename") # Fields you want to display in the list view
    search_fields = ('user__username', 'filename')  # Search by user or filename
    list_filter = ('uploaded_at',)  # Filter by upload date if needed


