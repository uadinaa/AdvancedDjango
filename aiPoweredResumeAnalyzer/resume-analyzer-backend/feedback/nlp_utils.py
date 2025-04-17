import spacy
from typing import List, Dict
from collections import Counter

nlp = spacy.load("en_core_web_sm")

# Sample list of trending skills (you can expand this)
TRENDING_SKILLS = {"python", "django", "react", "machine learning", "sql", "git", "docker"}


def extract_skills(text: str) -> List[str]:
    doc = nlp(text.lower())
    tokens = [token.text for token in doc if not token.is_stop and not token.is_punct]
    return list(set(tokens) & TRENDING_SKILLS)


def detect_skill_gaps(resume_skills: List[str]) -> List[str]:
    return list(TRENDING_SKILLS - set(resume_skills))


def suggest_keywords(job_description: str, resume_text: str) -> List[str]:
    job_doc = nlp(job_description.lower())
    resume_doc = nlp(resume_text.lower())
    job_words = set([token.lemma_ for token in job_doc if token.is_alpha])
    resume_words = set([token.lemma_ for token in resume_doc if token.is_alpha])
    return list(job_words - resume_words)


def check_formatting_sections(text: str) -> List[str]:
    expected_sections = ["experience", "education", "skills", "projects", "certifications"]
    feedback = []
    lowered = text.lower()
    for section in expected_sections:
        if section not in lowered:
            feedback.append(f"Missing section: {section.capitalize()}")
    return feedback
