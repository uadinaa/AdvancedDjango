from django import forms
from .models import Contact, Profile, CV

# ModelForm for Contact model
class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'message']

# ModelForm for Profile model
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'

class CVForm(forms.ModelForm):
    class Meta:
        model = CV
        fields = ['name', 'email', 'profile_picture']

