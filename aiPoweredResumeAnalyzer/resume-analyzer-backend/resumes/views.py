import os
import pdfplumber
import docx
import spacy
from rest_framework import generics, permissions
from rest_framework.response import Response
from pymongo import MongoClient
from .models import Resume
from .serializers import ResumeUploadSerializer
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from bson.objectid import ObjectId
from django.conf import settings
from rest_framework import generics
# from .nlp_utils import (
#     extract_skills, detect_skill_gaps, suggest_keywords, check_formatting_sections
# )

nlp = spacy.load("en_core_web_sm")

# Connect to MongoDB
mongo_client = MongoClient("mongodb://localhost:27017/")
mongo_db = mongo_client["resume_db"]
parsed_collection = mongo_db["parsed_resumes"]
client = MongoClient(settings.MONGO_URI)
mongo_db = client["resumes_db"]
resumes_collection = mongo_db["resumes"]

COMMON_SECTIONS = ["Education", "Experience", "Skills", "Projects", "Certifications"]

TOP_TRENDING_SKILLS = [
    "Python", "SQL", "Machine Learning", "Docker", "AWS", "JavaScript",
    "Git", "REST APIs", "React", "Django", "FastAPI"
]


def extract_text(file_path):
    text = ""
    ext = os.path.splitext(file_path)[1].lower()
    if ext == ".pdf":
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() + "\n"
    elif ext == ".docx":
        doc = docx.Document(file_path)
        for para in doc.paragraphs:
            text += para.text + "\n"
    return text


def parse_resume(text):
    doc = nlp(text)
    skills = [ent.text for ent in doc.ents if ent.label_ == "SKILL"]  # Custom rule needed
    education = [sent.text for sent in doc.sents if "university" in sent.text.lower()]
    experience = [sent.text for sent in doc.sents if "experience" in sent.text.lower()]
    return {
        "skills": skills,
        "education": education,
        "experience": experience,
        "raw_text": text
    }


class ResumeUploadView(generics.CreateAPIView):
    queryset = Resume.objects.all()
    serializer_class = ResumeUploadSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        resume = serializer.save(user=self.request.user)
        file_path = resume.file.path
        text = extract_text(file_path)
        parsed_data = parse_resume(text)
        parsed_data.update({
            "user_id": str(self.request.user.id),
            "resume_id": str(resume.id)
        })
        parsed_collection.insert_one(parsed_data)
        parsed_collection.update_one(
            {"user_id": str(self.request.user.id)},
            {"$set": {
                **parsed_data,
                "user_id": str(self.request.user.id),
                "resume_id": str(resume.id)
            }},
            upsert=True
        )


class ResumeFeedbackView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_id = str(request.user.id)

        mongo_client = MongoClient("mongodb://localhost:27017/")
        parsed_resume = mongo_client["resume_db"]["parsed_resumes"].find_one({"user_id": user_id})

        if not parsed_resume:
            return Response({"error": "No parsed resume found."}, status=404)

        feedback = {
            "skill_gaps": [],
            "formatting_tips": [],
            "ats_keywords": [],
        }

        # --- Skill Gaps ---
        user_skills = set(parsed_resume.get("skills", []))
        trending_skills = set(TOP_TRENDING_SKILLS)
        missing = list(trending_skills - user_skills)
        feedback["skill_gaps"] = missing

        # --- Formatting Tips ---
        resume_text = parsed_resume.get("raw_text", "")
        if len(resume_text.split()) > 1000:
            feedback["formatting_tips"].append("Your resume is quite long. Consider shortening it to 1–2 pages.")
        if not any(section.lower() in resume_text.lower() for section in COMMON_SECTIONS):
            feedback["formatting_tips"].append("Missing common sections like Education, Experience, or Skills.")
        if resume_text.count("\n") < 10:
            feedback["formatting_tips"].append("Consider using more line breaks for readability.")

        # --- ATS Keyword Matching ---
        # (Assuming user applied to job_id=1 — you can pass this via query param later)
        job_desc = "Looking for Python, Django, REST APIs, and AWS experience."
        job_keywords = set(job_desc.lower().split())
        resume_words = set(resume_text.lower().split())
        matched_keywords = list(job_keywords & resume_words)
        feedback["ats_keywords"] = matched_keywords

        return Response(feedback)


class ResumeParsedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_id = str(request.user.id)

        mongo_client = MongoClient("mongodb://localhost:27017/")
        parsed_collection = mongo_client["resume_db"]["parsed_resumes"]

        resume_data = parsed_collection.find_one({"user_id": user_id})
        if not resume_data:
            return Response({"message": "No parsed resume found."}, status=404)

        resume_data.pop('_id', None)
        return Response(resume_data)

    def patch(self, request):
        user_id = str(request.user.id)
        update_data = request.data

        mongo_client = MongoClient("mongodb://localhost:27017/")
        parsed_collection = mongo_client["resume_db"]["parsed_resumes"]

        result = parsed_collection.update_one(
            {"user_id": user_id},
            {"$set": update_data},
            upsert=False  # Don’t create if not exists
        )

        if result.matched_count == 0:
            return Response({"message": "Resume not found."}, status=404)

        return Response({"message": "Resume updated successfully."}, status=status.HTTP_200_OK)


class ResumeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role == 'job_seeker':
            resume = Resume.objects.filter(user=request.user).first()
            if resume:
                return Response({"resume": resume.filename})
            return Response({"message": "No resume found."}, status=404)

        # Admins can view all resumes
        if request.user.role == 'admin':
            resumes = Resume.objects.all()
            return Response({"resumes": [resume.filename for resume in resumes]})

        return Response({"message": "Access Denied."}, status=403)


class ResumeDeleteView(generics.DestroyAPIView):
    serializer_class = ResumeUploadSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return Resume.objects.all()
        return Resume.objects.filter(user=user)


class ResumeDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        resume = parsed_collection.find_one({"user_id": str(request.user.id)})
        if not resume:
            return Response({"error": "No resume found"}, status=404)

        return Response({
            "file_name": resume.get("file_name", "unknown"),
            "raw_text": resume.get("raw_text", "")
        })


class ResumeListView(generics.ListAPIView):
    serializer_class = ResumeUploadSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return Resume.objects.all()
        return Resume.objects.filter(user=user)
