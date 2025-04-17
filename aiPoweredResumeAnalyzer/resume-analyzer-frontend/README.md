#  CV Analyzer by AI

An AI-powered resume analysis platform that allows users to upload resumes, receive instant feedback, and match with relevant job descriptions. The system uses NLP techniques to evaluate resumes and provides insights for both applicants and recruiters.

## Features

-  **User Registration & Role-Based Auth**  
  Users can register as `user`, `admin`, or `recruiter`. Email verification and JWT-based login are implemented.

- **Resume Upload & Parsing**  
  Users can upload `.pdf` or `.docx` resumes. The system parses content and stores it in MongoDB.

- **AI Resume Rating**  
  Resumes are scored using NLP techniques (TF-IDF, cosine similarity) and evaluated for job match accuracy, skill gaps, and ATS optimization.

- **Feedback System**  
  Personalized feedback includes missing skills, formatting issues, and tips to improve the resume.

- **Job Matching System**  
  Match resumes to job descriptions and get the most relevant job postings using similarity metrics.

- **Admin Dashboard**  
  Admins can view user lists, manage jobs/resumes, and moderate the platform.

- **Recruiter Tools**  
  Recruiters can post jobs, view parsed resumes, and filter by AI-generated match score.

- **Result History & Filtering**  
  All resume scores and job matches are timestamped and can be filtered, paginated, or exported.

---

## Tech Stack

- **Frontend**: Vue.js + Vuetify  
- **Backend**: Django + Django REST Framework  
- **Database**: PostgreSQL (users, jobs) + MongoDB (resumes)  
- **AI/NLP**: Python (spaCy / NLTK / Scikit-learn)  
- **Auth**: JWT (access/refresh tokens)  
- **Email**: SMTP with Django `send_mail()`  
- **Asynchronous Tasks**: Celery + Redis

---

## Demo

![Demo Screenshot](https://drive.google.com/drive/folders/1FOAoXyIb1E5AgqryZereaACMHwtpbd3D?usp=sharing)


---

## User Roles

| Role          | Permissions                                  |
|---------------|----------------------------------------------|
| **User**      | Upload resumes, view matches & feedback      |
| **Admin**     | Manage users, jobs, resumes, and permissions |
| **Recruiter** | Post jobs, match resumes to job listings     |


## API Endpoints (Sample)

POST /api/auth/register/
POST /api/auth/login/
GET /api/resumes/
POST /api/resumes/upload/
POST /api/resumes/match/
GET /api/users/ (admin only)

