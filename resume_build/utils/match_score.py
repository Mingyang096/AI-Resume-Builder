from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
from ..skills_config import HARD_SKILLS, SOFT_SKILLS, OTHER_KEYWORDS


def calculate_category_match(category_keywords, content):
    """
    Calculate match percentage for a specific category of keywords.
    Args:
        category_keywords (list): List of keywords for the category.
        content (str): The content to match the keywords against.
    Returns:
        float: Match percentage (0-100).
    """
    if not category_keywords:  # Handle empty keywords list
        return 0.0
    
    if not content.strip():  # Ensure content is not empty
        return 0.0
    
    # Preprocess content and keywords
    content = content.lower()
    content = ' '.join(set(content.lower().split()))  # Remove redundancy in content
    category_keywords = [keyword.lower() for keyword in category_keywords]
    
    # Vectorize content and keywords
    vectorizer = CountVectorizer(vocabulary=category_keywords)
    content_vector = vectorizer.fit_transform([content])
    category_vector = vectorizer.transform([' '.join(category_keywords)])
    
    # Debugging: Check vectors
    # print("Category Keywords Vector:", category_vector.toarray())
    # print("Content Vector:", content_vector.toarray())
    
    # Compute cosine similarity
    similarity = cosine_similarity(content_vector, category_vector)[0][0]
    # print("Cosine Similarity:", similarity)
    
    return round(similarity * 100, 2)


def extract_skills_from_text(text, skills):
    """
    Extract relevant skills from text based on a predefined list of skills.
    """
    if not text:
        return []
    text_lower = text.lower()
    relevant_skills = [skill for skill in skills if skill.lower() in text_lower]
    return relevant_skills


def calculate_skill_scores(job, raw_content, processed_content):
    """
    Calculate scores and reports for hard skills, soft skills, and keywords.
    """
    skill_categories = {
        "Hard Skills": HARD_SKILLS,
        "Soft Skills": SOFT_SKILLS,
        "Keywords": OTHER_KEYWORDS,
    }

    scores_and_reports = {}
    # job = type("Job", (object,), {"description": "Expert in Python and SQL"})()  # Mock object
    # scores = calculate_skill_scores(hard_skills, resume_content, processed_content)
    for category, skills in skill_categories.items():
        # Extract job-relevant skills
        job_relevant_skills = extract_skills_from_text(job.description, skills)
        # print("job_relevant_skills")
        # print(job_relevant_skills)

        if not job_relevant_skills:
            # print("No skills extracted")
            raw_score = 0.0
            processed_score = 0.0
            raw_report = f"No {category.lower()} extracted from the job description."
            processed_report = raw_report
        else:
            raw_score = calculate_category_match(job_relevant_skills, raw_content)
            processed_score = calculate_category_match(job_relevant_skills, processed_content)
            processed_score = max(processed_score, raw_score)

            missing_raw = [skill for skill in job_relevant_skills if skill.lower() not in raw_content.lower()]
            missing_processed = [skill for skill in job_relevant_skills if skill.lower() not in processed_content.lower()]

            raw_report = (
                f"Great work! You have most of the {category.lower()} required for this job."
                if not missing_raw
                else f"You are missing {len(missing_raw)} {category.lower()}: {', '.join(missing_raw)}."
            )

            processed_report = (
                f"Great work! You have most of the {category.lower()} required for this job."
                if not missing_processed
                else f"You are missing {len(missing_processed)} {category.lower()}: {', '.join(missing_processed)}."
            )

        scores_and_reports[category] = {
            "raw_score": raw_score,
            "processed_score": processed_score,
            "raw_report": raw_report,
            "processed_report": processed_report,
        }

    return scores_and_reports


def calculate_title_degree_scores(content, job):
    """
    Calculate degree and title match scores.

    Args:
        content (str): The text content to analyze (e.g., resume or description).
        job (object): An object containing job details, including job description and job title.

    Returns:
        tuple: A tuple of (degree_score, title_score) where each score is 0-100.
    """
    if not job.job_title.strip():
        raise ValueError("Job title cannot be empty.")

    # Degrees to match
    degree_keywords = ["master", "phd", "bachelor"]

    # Convert to lowercase for case-insensitive comparison
    content_lower = content.lower()
    job_description_lower = job.description.lower()

    # Calculate degree score
    degree_score = 0
    for degree in degree_keywords:
        if degree in job_description_lower and degree in content_lower:
            degree_score = 100
            break

    # Calculate title score
    title_score = 100 if job.job_title.lower() in content_lower else 0

    return degree_score, title_score


def calculate_overall_score(hard, soft, keywords, degree, title):
    """
    Calculate overall match score based on weighted averages.
    """
    return round((hard * 0.4) + (soft * 0.2) + (keywords * 0.2) + (degree * 0.1) + (title * 0.1), 2)


def generate_title_degree_report(score, category, job, content):
    """
    Generate a report for the title or degree match.

    Args:
        score (int): The match score (0 or 100).
        category (str): The category being evaluated ("Title" or "Degree").
        job (object): An object containing job details, including job description and job title.
        content (str): The text content to analyze (e.g., resume or description).

    Returns:
        str: A report explaining the match or lack thereof.
    """
    if category.lower() == "degree":
        # Degrees to match
        degree_keywords = ["master", "phd", "bachelor"]
        content_lower = content.lower()
        job_description_lower = job.description.lower()

        # Identify missing degrees
        missing_degrees = [
            degree for degree in degree_keywords
            if degree in job_description_lower and degree not in content_lower
        ]
        return (
            f"Great work! The {category.lower()} matches your resume perfectly."
            if score == 100
            else f"You are missing these degrees mentioned in the job description: {', '.join(missing_degrees)}."
            if missing_degrees
            else "No relevant degree requirements found in the job description."
        )

    elif category.lower() == "title":
        return (
            f"Great work! The {category.lower()} matches your resume perfectly."
            if score == 100
            else f"Your resume does not include the job title '{job.job_title}'. Consider aligning your title."
        )

    else:
        return f"Invalid category: {category}. Please use 'Title' or 'Degree'."
