import os
import logging
import tempfile
from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from modules.validator import validate_file
from modules.parser import parse_resume
from modules.analyzer import analyze_resume
from modules.scorer import calculate_ats_score

# Load environment variables
load_dotenv()

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# FastAPI app
app = FastAPI(
    title="AI Resume Analyzer",
    description="Analyze resumes using Gemini AI",
    version="1.0.0"
)

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    """Health check endpoint."""
    return {"message": "AI Resume Analyzer API is running!"}


@app.post("/analyze")
async def analyze(
    file: UploadFile = File(...),
    job_description: str = Form(...)
):
    """
    Main endpoint - upload resume and job description.
    Returns ATS score, matched skills, missing skills, and suggestions.
    """
    try:
        # Step 1: Read file
        file_content = await file.read()
        file_size = len(file_content)

        # Step 2: Validate file
        logger.info(f"Validating file: {file.filename}")
        validation = validate_file(file.filename, file_size)
        if not validation["valid"]:
            raise HTTPException(status_code=400, detail=validation["error"])

        # Step 3: Save temp file and parse
        logger.info("Parsing resume...")
        suffix = os.path.splitext(file.filename)[1]
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp.write(file_content)
            tmp_path = tmp.name

        resume_text = parse_resume(tmp_path)
        os.unlink(tmp_path)  # Delete temp file

        if not resume_text:
            raise HTTPException(status_code=400, detail="Could not extract text from resume.")

        # Step 4: Calculate ATS score
        logger.info("Calculating ATS score...")
        ats_result = calculate_ats_score(resume_text)

        # Step 5: AI Analysis
        logger.info("Running AI analysis...")
        ai_result = analyze_resume(resume_text, job_description)

        # Step 6: Return combined result
        return {
            "filename": file.filename,
            "word_count": ats_result["word_count"],
            "ats_score": ai_result["ats_score"],
            "job_match": ai_result["job_match"],
            "matched_skills": ai_result["matched_skills"],
            "missing_skills": ai_result["missing_skills"],
            "suggestions": ai_result["suggestions"],
            "ats_feedback": ats_result["feedback"]
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")