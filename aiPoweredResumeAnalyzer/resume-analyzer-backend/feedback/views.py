from rest_framework.views import APIView
from rest_framework.response import Response
from pymongo import MongoClient
from rest_framework.permissions import IsAuthenticated
from bson.objectid import ObjectId
from django.conf import settings
from .resume_rater import calculate_match_score
from django.shortcuts import render
import requests
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
import csv
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from io import BytesIO
from .forms import ResumeUploadForm
from .nlp_utils import (
    extract_skills, detect_skill_gaps, suggest_keywords, check_formatting_sections
)


client = MongoClient(settings.MONGO_URI)
mongo_db = client["resumes_db"]
resumes_collection = mongo_db["resumes"]
ratings_collection = mongo_db["ratings"]


class ResumeFeedbackView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        resume_text = request.data.get("resume_text")
        job_description = request.data.get("job_description")

        if not resume_text or not job_description:
            return Response({"error": "resume_text and job_description are required."}, status=400)

        skills = extract_skills(resume_text)
        skill_gaps = detect_skill_gaps(skills)
        formatting_issues = check_formatting_sections(resume_text)
        keyword_suggestions = suggest_keywords(job_description, resume_text)

        return Response({
            "extracted_skills": skills,
            "skill_gaps": skill_gaps,
            "formatting_feedback": formatting_issues,
            "keyword_suggestions": keyword_suggestions
        })


class ResumeFeedbackFromMongoView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        resume_id = request.data.get("resume_id")
        job_description = request.data.get("job_description")

        if not resume_id or not job_description:
            return Response({"error": "resume_id and job_description are required."}, status=400)

        try:
            resume_doc = resumes_collection.find_one({"_id": ObjectId(resume_id)})
            resume_text = resume_doc.get("text", "")
        except Exception as e:
            return Response({"error": "Could not retrieve resume text."}, status=500)

        if not resume_text:
            return Response({"error": "Resume text is empty or not found."}, status=404)

        # NLP Feedback
        skills = extract_skills(resume_text)
        skill_gaps = detect_skill_gaps(skills)
        formatting_issues = check_formatting_sections(resume_text)
        keyword_suggestions = suggest_keywords(job_description, resume_text)

        return Response({
            "extracted_skills": skills,
            "skill_gaps": skill_gaps,
            "formatting_feedback": formatting_issues,
            "keyword_suggestions": keyword_suggestions
        })


class ResumeRatingView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        resume_text = request.data.get("resume_text")
        job_description = request.data.get("job_description")

        if not resume_text or not job_description:
            return Response({"error": "resume_text and job_description are required"}, status=400)

        score_data = calculate_match_score(resume_text, job_description)

        return Response({
            "resume_rating": score_data
        })


class ResumeRatingFromMongoView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        resume_id = request.data.get("resume_id")
        job_description = request.data.get("job_description")

        if not resume_id or not job_description:
            return Response({"error": "resume_id and job_description are required"}, status=400)

        try:
            resume_doc = resumes_collection.find_one({"_id": ObjectId(resume_id)})
            if not resume_doc:
                return Response({"error": "Resume not found"}, status=404)
            resume_text = resume_doc.get("text", "")
        except Exception as e:
            return Response({"error": str(e)}, status=500)

        score_data = calculate_match_score(resume_text, job_description)

        if request.user.is_authenticated:
            user_email = request.user.email

            rating_result = {
                "resume_id": resume_id,
                "user_email": user_email,
                "job_description": job_description,
                "keyword_score": score_data.get("keyword_score"),
                "skill_score": score_data.get("skill_score"),
                "final_score": score_data.get("final_score"),
                "timestamp": datetime.utcnow().isoformat()
            }

            # Save rating result in a separate MongoDB collection (e.g., ratings)
            mongo_db["ratings"].insert_one(rating_result)

        rating_result = {
            "resume_id": resume_id,
            "job_description": job_description,
            "keyword_score": score_data.get("keyword_score"),
            "skill_score": score_data.get("skill_score"),
            "final_score": score_data.get("final_score"),
            "timestamp": datetime.utcnow().isoformat()  # <-- this is the timestamp
        }

        ratings_collection.insert_one(rating_result)

        return Response({
            "resume_id": resume_id,
            "rating_result": score_data
        })


def test_rating_view(request):
    mock_rating = {
        "keyword_score": 75.0,
        "skill_score": 80.0,
        "final_score": 77.5
    }
    return render(request, "feedback/rating_result.html", {"rating": mock_rating})


@csrf_exempt  # If you’re testing without JWT for now
def rating_form_view(request):
    rating_data = None

    if request.method == 'POST':
        resume_id = request.POST.get('resume_id')
        job_desc = request.POST.get('job_description')

        try:
            api_url = 'http://localhost:8000/api/feedback/rate/from-mongo/'
            payload = {
                "resume_id": resume_id,
                "job_description": job_desc
            }

            # If using JWT later, send with headers
            headers = {'Content-Type': 'application/json'}
            response = requests.post(api_url, json=payload, headers=headers)

            if response.status_code == 200:
                rating_data = response.json().get('rating_result', {})
            else:
                rating_data = {"error": "API error: " + str(response.status_code)}

        except Exception as e:
            rating_data = {"error": str(e)}

    return render(request, "feedback/rating_form.html", {"rating": rating_data})


@csrf_exempt
def view_rating_history(request):
    rating = None
    resume_id = None

    if request.method == 'POST':
        resume_id = request.POST.get('resume_id')

        try:
            response = requests.get(f'http://localhost:8000/api/feedback/rate/from-mongo/{resume_id}/')

            if response.status_code == 200:
                rating = response.json().get('rating_result')
            else:
                rating = {"error": f"Rating not found. Status: {response.status_code}"}

        except Exception as e:
            rating = {"error": str(e)}

    return render(request, "feedback/rating_history.html", {"rating": rating, "resume_id": resume_id})


@login_required
def my_rating_history(request):
    client = MongoClient("mongodb://localhost:27017/")
    db = client["your_mongo_db"]
    collection = db["resume_ratings"]

    user_email = request.user.email
    query = {"user_email": user_email}

    # Filters from query params
    min_score = request.GET.get("min_score")
    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")

    if min_score:
        query["final_score"] = {"$gte": float(min_score)}

    if start_date or end_date:
        query["timestamp"] = {}
        if start_date:
            query["timestamp"]["$gte"] = datetime.fromisoformat(start_date)
        if end_date:
            query["timestamp"]["$lte"] = datetime.fromisoformat(end_date)

    ratings = list(collection.find(query).sort("timestamp", -1))

    paginator = Paginator(ratings, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "feedback/my_ratings.html", {
        "page_obj": page_obj,
        "filters": {
            "min_score": min_score,
            "start_date": start_date,
            "end_date": end_date,
        }
    })

@login_required
def export_ratings_csv(request):
    client = MongoClient("mongodb://localhost:27017/")
    db = client["your_mongo_db"]
    collection = db["resume_ratings"]

    user_email = request.user.email
    ratings = list(collection.find({"user_email": user_email}))

    response = HttpResponse(content_type="text/csv")
    response['Content-Disposition'] = 'attachment; filename="resume_ratings.csv"'

    writer = csv.writer(response)
    writer.writerow(["Resume ID", "Keyword Score", "Skill Score", "Final Score", "Timestamp"])

    for r in ratings:
        writer.writerow([
            r.get("resume_id", ""),
            r.get("keyword_score", ""),
            r.get("skill_score", ""),
            r.get("final_score", ""),
            r.get("timestamp", "")
        ])

    return response


@login_required
def export_ratings_pdf(request):
    client = MongoClient("mongodb://localhost:27017/")
    db = client["your_mongo_db"]
    collection = db["resume_ratings"]

    user_email = request.user.email
    ratings = list(collection.find({"user_email": user_email}))

    buffer = BytesIO()
    p = canvas.Canvas(buffer)
    y = 800
    p.setFont("Helvetica", 12)

    p.drawString(100, y, "My Resume Ratings Report")
    y -= 30

    for r in ratings:
        line = f"Resume ID: {r.get('resume_id', '')} | Keyword: {r.get('keyword_score', '')}% | Skill: {r.get('skill_score', '')}% | Final: {r.get('final_score', '')}% | Date: {r.get('timestamp', '')}"
        p.drawString(50, y, line)
        y -= 20
        if y < 50:
            p.showPage()
            y = 800

    p.save()
    buffer.seek(0)
    return HttpResponse(buffer, content_type="application/pdf")

