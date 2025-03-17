from django.db import models
from django import forms

class Profile(models.Model):
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    phone = models.CharField(max_length=200)
    summary = models.TextField(max_length=2000)
    degree = models.CharField(max_length=200)
    school = models.CharField(max_length=200)
    university = models.CharField(max_length=200)
    previous_work = models.TextField(max_length=1000)
    skills = models.TextField(max_length=1000)
    employed = models.BooleanField(default=False)


class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()


class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)


class CV(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)

