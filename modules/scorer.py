import logging

logger = logging.getLogger(__name__)


def calculate_ats_score(resume_text: str) -> dict:
    """
    Calculate ATS friendliness score based on resume formatting.
    Checks for important sections and keywords.
    """
    try:
        score = 0
        feedback = []
        resume_lower = resume_text.lower()

        # Check important sections (40 points)
        sections = {
            "experience": 10,
            "education": 10,
            "skills": 10,
            "projects": 5,
            "certifications": 5
        }

        for section, points in sections.items():
            if section in resume_lower:
                score += points
                feedback.append(f"✅ '{section.title()}' section found")
            else:
                feedback.append(f"❌ '{section.title()}' section missing")

        # Check contact information (30 points)
        if "@" in resume_text:
            score += 10
            feedback.append("✅ Email address found")
        else:
            feedback.append("❌ Email address missing")

        if any(char.isdigit() for char in resume_text):
            score += 10
            feedback.append("✅ Phone number found")
        else:
            feedback.append("❌ Phone number missing")

        if "linkedin" in resume_lower or "github" in resume_lower:
            score += 10
            feedback.append("✅ LinkedIn/GitHub profile found")
        else:
            feedback.append("❌ LinkedIn/GitHub profile missing")

        # Check resume length (30 points)
        word_count = len(resume_text.split())
        if word_count >= 300:
            score += 15
            feedback.append(f"✅ Good resume length ({word_count} words)")
        else:
            feedback.append(f"❌ Resume too short ({word_count} words). Aim for 300+ words")

        if word_count <= 800:
            score += 15
            feedback.append("✅ Resume length is concise")
        else:
            feedback.append("⚠️ Resume might be too long. Keep it under 800 words")

        logger.info(f"ATS score calculated: {score}")
        return {
            "ats_score": score,
            "feedback": feedback,
            "word_count": word_count
        }

    except Exception as e:
        logger.error(f"Error calculating ATS score: {e}")
        raise ValueError(f"Score calculation failed: {e}")