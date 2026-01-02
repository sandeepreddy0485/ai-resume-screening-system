import re
from fastapi import FastAPI
from pydantic import BaseModel
from database import Base, engine
from models import User

app = FastAPI(title="AI Resume Screening API")


# ------------------ Resume Logic ------------------

def extract_skills(text):
    skill_keywords = [
        "python", "java", "machine learning", "ai", "nlp",
        "sql", "react", "fastapi", "flask", "django"
    ]
    return list(set([s for s in skill_keywords if s in text.lower()]))


def extract_education(text):
    keywords = ["b.tech", "bachelor", "master", "degree", "engineering"]
    return [line for line in text.lower().split("\n") if any(k in line for k in keywords)]


def extract_experience(text):
    return [line for line in text.split("\n") if "intern" in line.lower()]


def parse_resume(text):
    return {
        "skills": extract_skills(text),
        "education": extract_education(text),
        "experience": extract_experience(text)
    }


def calculate_match_score(resume_skills, job_text):
    matched = [s for s in resume_skills if s in job_text.lower()]
    score = (len(matched) / len(resume_skills)) * 100 if resume_skills else 0
    return round(score, 2), matched


def final_weighted_score(parsed_resume, job_text):
    skill_score, matched_skills = calculate_match_score(parsed_resume["skills"], job_text)
    edu_score = 100 if parsed_resume["education"] else 0
    exp_score = 100 if parsed_resume["experience"] else 0

    final = 0.6 * skill_score + 0.2 * edu_score + 0.2 * exp_score
    return round(final, 2), matched_skills


# ------------------ API Models ------------------

class ResumeRequest(BaseModel):
    resume_text: str
    job_description: str

class BulkResumeRequest(BaseModel):
    resumes: list[str]
    job_description: str


# ------------------ API Endpoints ------------------
Base.metadata.create_all(bind=engine)
@app.get("/")
def home():
    return {"message": "AI Resume Screening API is running"}


@app.post("/match")
def match_resume(data: ResumeRequest):
    parsed = parse_resume(data.resume_text)
    score, matched = final_weighted_score(parsed, data.job_description)

    return {
        "score": score,
        "matched_skills": matched,
        "parsed_resume": parsed
    }
@app.post("/rank")
def rank_resumes(data: BulkResumeRequest):
    results = []

    for idx, resume_text in enumerate(data.resumes):
        parsed = parse_resume(resume_text)
        score, matched = final_weighted_score(parsed, data.job_description)

        results.append({
            "resume_id": idx + 1,
            "score": score,
            "matched_skills": matched
        })

    # sort by score (highest first)
    results.sort(key=lambda x: x["score"], reverse=True)

    return {
        "job_description": data.job_description,
        "ranked_resumes": results
    }

