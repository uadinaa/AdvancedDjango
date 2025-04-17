import spacy
from collections import Counter

nlp = spacy.load("en_core_web_sm")

TRENDING_SKILLS = {"python", "django", "react", "sql", "docker", "machine learning", "git"}


def tokenize(text):
    doc = nlp(text.lower())
    return [token.lemma_ for token in doc if token.is_alpha and not token.is_stop]


def calculate_match_score(resume_text, job_description):
    resume_tokens = set(tokenize(resume_text))
    job_tokens = set(tokenize(job_description))

    # Keyword match
    common_keywords = resume_tokens & job_tokens
    keyword_score = (len(common_keywords) / len(job_tokens)) * 100 if job_tokens else 0

    # Skill match
    resume_skills = resume_tokens & TRENDING_SKILLS
    job_skills = job_tokens & TRENDING_SKILLS
    skill_score = (len(resume_skills & job_skills) / len(job_skills)) * 100 if job_skills else 0

    # Final score: 50% keyword + 50% skill
    final_score = round((keyword_score * 0.5) + (skill_score * 0.5), 2)

    return {
        "keyword_score": round(keyword_score, 2),
        "skill_score": round(skill_score, 2),
        "final_score": final_score
    }