from django import forms


class ResumeUploadForm(forms.Form):
    resume = forms.FileField(label='Resume File (PDF or DOCX)', required=True)
