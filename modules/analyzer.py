import os
import logging
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def analyze_resume(resume_text: str, job_description: str) -> dict:
    """Use Groq AI to analyze resume against job description."""
    try:
        prompt = f"""
You are an expert ATS resume analyzer.

Analyze the following resume against the job description and provide:

Resume:
{resume_text}

Job Description:
{job_description}

Respond in this EXACT format:
ATS_SCORE: [number 0-100]
JOB_MATCH: [number 0-100]
MATCHED_SKILLS: [comma separated list]
MISSING_SKILLS: [comma separated list]
SUGGESTIONS:
- [suggestion 1]
- [suggestion 2]
- [suggestion 3]
- [suggestion 4]
- [suggestion 5]
"""

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )

        result_text = response.choices[0].message.content
        logger.info("Groq AI analysis completed successfully")
        return parse_ai_response(result_text)

    except Exception as e:
        logger.error(f"Error in AI analysis: {e}")
        raise ValueError(f"AI analysis failed: {e}")


def parse_ai_response(response_text: str) -> dict:
    """Parse AI response into structured dictionary."""
    try:
        lines = response_text.strip().split("\n")
        result = {
            "ats_score": 0,
            "job_match": 0,
            "matched_skills": [],
            "missing_skills": [],
            "suggestions": []
        }

        suggestions_section = False

        for line in lines:
            line = line.strip()
            if line.startswith("ATS_SCORE:"):
                result["ats_score"] = int(line.split(":")[1].strip())
            elif line.startswith("JOB_MATCH:"):
                result["job_match"] = int(line.split(":")[1].strip())
            elif line.startswith("MATCHED_SKILLS:"):
                skills = line.split(":")[1].strip()
                result["matched_skills"] = [s.strip() for s in skills.split(",")]
            elif line.startswith("MISSING_SKILLS:"):
                skills = line.split(":")[1].strip()
                result["missing_skills"] = [s.strip() for s in skills.split(",")]
            elif line.startswith("SUGGESTIONS:"):
                suggestions_section = True
            elif suggestions_section and line.startswith("-"):
                result["suggestions"].append(line[1:].strip())

        return result

    except Exception as e:
        logger.error(f"Error parsing AI response: {e}")
        raise ValueError(f"Could not parse AI response: {e}")