from rest_framework import serializers
from .models import Resume
from rest_framework import serializers


class ResumeUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resume
        fields = '__all__'


