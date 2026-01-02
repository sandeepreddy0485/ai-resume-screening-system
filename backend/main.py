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


if __name__ == "__main__":
    resume_text = read_resume("sample_resume.txt")
    parsed_data = parse_resume(resume_text)

    print("\nParsed Resume Data:")
    print(parsed_data)
