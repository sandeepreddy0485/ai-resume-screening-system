import re


def read_resume(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()


def extract_skills(text):
    skill_keywords = [
        "python", "java", "machine learning", "ai", "nlp",
        "sql", "react", "fastapi", "flask", "django"
    ]
    found_skills = []

    text_lower = text.lower()
    for skill in skill_keywords:
        if skill in text_lower:
            found_skills.append(skill)

    return list(set(found_skills))


def extract_education(text):
    education_keywords = ["b.tech", "bachelor", "master", "degree", "engineering"]
    education = []

    lines = text.lower().split("\n")
    for line in lines:
        for word in education_keywords:
            if word in line:
                education.append(line.strip())

    return education


def extract_experience(text):
    experience = []
    lines = text.split("\n")
    for line in lines:
        if "intern" in line.lower() or "experience" in line.lower():
            experience.append(line.strip())
    return experience


def parse_resume(text):
    return {
        "skills": extract_skills(text),
        "education": extract_education(text),
        "experience": extract_experience(text)
    }


def calculate_match_score(resume_skills, job_text):
    job_text = job_text.lower()

    matched_skills = []
    for skill in resume_skills:
        if skill.lower() in job_text:
            matched_skills.append(skill)

    if not resume_skills:
        return 0, []

    score = (len(matched_skills) / len(resume_skills)) * 100
    return round(score, 2), matched_skills
def education_match_score(education_list, job_text):
    if not education_list:
        return 0

    job_text = job_text.lower()
    matched = 0

    for edu in education_list:
        if edu.lower() in job_text:
            matched += 1

    return min((matched / len(education_list)) * 100, 100)


def experience_match_score(experience_list, job_text):
    if not experience_list:
        return 0

    job_text = job_text.lower()
    matched = 0

    for exp in experience_list:
        if "intern" in exp.lower() and "intern" in job_text:
            matched += 1

    return min((matched / len(experience_list)) * 100, 100)
def final_weighted_score(parsed_resume, job_text):
    skill_score, matched_skills = calculate_match_score(
        parsed_resume["skills"], job_text
    )

    edu_score = education_match_score(
        parsed_resume["education"], job_text
    )

    exp_score = experience_match_score(
        parsed_resume["experience"], job_text
    )

    final_score = (
        0.6 * skill_score +
        0.2 * edu_score +
        0.2 * exp_score
    )

    return round(final_score, 2), matched_skills


if __name__ == "__main__":
    resume_text = read_resume("sample_resume.txt")
    job_text = read_resume("job_description.txt")

    parsed_resume = parse_resume(resume_text)
    final_score, matched = final_weighted_score(
    parsed_resume, job_text
    )
    print("\nFINAL MATCH RESULT")
    print(f"Final Score: {final_score}%")
    print(f"Matched Skills: {matched}")
    