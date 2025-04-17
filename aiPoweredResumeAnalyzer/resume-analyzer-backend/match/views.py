from rest_framework.views import APIView
from rest_framework.response import Response
from pymongo import MongoClient
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from rest_framework.permissions import IsAuthenticated
from users.permissions import IsAdmin, IsRecruiter
from jobs.models import JobDescription
from jobs.serializers import JobDescriptionSerializer

mongo_client = MongoClient("mongodb://localhost:27017/")
mongo_db = mongo_client["resume_db"]
parsed_collection = mongo_db["parsed_resumes"]

class MatchJobsView(APIView):
    permission_classes = [IsAuthenticated]  # Optional: Add IsJobSeeker

    def get(self, request, user_id):
        # Get parsed resume from MongoDB
        resume_data = parsed_collection.find_one({"user_id": str(user_id)})
        if not resume_data:
            return Response({"error": "No resume found for this user"}, status=404)

        resume_text = resume_data.get("raw_text", "")
        if not resume_text.strip():
            return Response({"error": "Resume text is empty"}, status=400)

        # Retrieve jobs
        jobs = JobDescription.objects.all()
        if not jobs.exists():
            return Response({"message": "No job descriptions available"}, status=404)

        job_texts = [job.description for job in jobs]
        job_ids = [job.id for job in jobs]
        job_infos = [(job.id, job.title, job.description) for job in jobs]


        # TF-IDF & similarity
        vectorizer = TfidfVectorizer()
        vectors = vectorizer.fit_transform([resume_text] + job_texts)
        similarities = cosine_similarity(vectors[0:1], vectors[1:]).flatten()

        results = []
        for i, score in enumerate(similarities):
            job_id, job_title, job_desc = job_infos[i]
            results.append({
                "job_id": job_id,
                "title": job_title,
                "description": job_desc,
                "score": round(float(score), 2)
            })

        sorted_results = sorted(results, key=lambda x: x["score"], reverse=True)
        return Response(sorted_results)
