import streamlit as st
import os
import tempfile
from groq import Groq
from dotenv import load_dotenv
import fitz
import docx

load_dotenv()

GROQ_API_KEY = "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"

st.set_page_config(page_title="AI Resume Analyzer", page_icon="📄", layout="centered")
st.title("📄 AI Resume Analyzer")
st.markdown("Upload your resume and get AI-powered analysis instantly!")
st.divider()

uploaded_file = st.file_uploader("Upload Resume (PDF or DOCX)", type=["pdf", "docx"])
job_description = st.text_area("Paste Job Description Here", height=200)

def extract_text(uploaded_file):
    suffix = "." + uploaded_file.name.split(".")[-1]
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = tmp.name
    if suffix == ".pdf":
        doc = fitz.open(tmp_path)
        text = "".join([page.get_text() for page in doc])
        doc.close()
    else:
        d = docx.Document(tmp_path)
        text = "\n".join([p.text for p in d.paragraphs])
    os.unlink(tmp_path)
    return text

def analyze(resume_text, job_description):
    prompt = f"""
You are an expert ATS resume analyzer.
Analyze the following resume against the job description.

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
    return response.choices[0].message.content

def parse_response(text):
    lines = text.strip().split("\n")
    result = {"ats_score": 0, "job_match": 0, "matched_skills": [], "missing_skills": [], "suggestions": []}
    suggestions_section = False
    for line in lines:
        line = line.strip()
        if line.startswith("ATS_SCORE:"):
            result["ats_score"] = int(line.split(":")[1].strip())
        elif line.startswith("JOB_MATCH:"):
            result["job_match"] = int(line.split(":")[1].strip())
        elif line.startswith("MATCHED_SKILLS:"):
            result["matched_skills"] = [s.strip() for s in line.split(":")[1].split(",")]
        elif line.startswith("MISSING_SKILLS:"):
            result["missing_skills"] = [s.strip() for s in line.split(":")[1].split(",")]
        elif line.startswith("SUGGESTIONS:"):
            suggestions_section = True
        elif suggestions_section and line.startswith("-"):
            result["suggestions"].append(line[1:].strip())
    return result

if st.button("🔍 Analyze Resume", use_container_width=True):
    if not uploaded_file:
        st.error("Please upload a resume!")
    elif not job_description.strip():
        st.error("Please enter a job description!")
    else:
        with st.spinner("Analyzing with AI..."):
            try:
                resume_text = extract_text(uploaded_file)
                ai_response = analyze(resume_text, job_description)
                result = parse_response(ai_response)

                st.success("✅ Analysis Complete!")
                st.divider()

                col1, col2 = st.columns(2)
                with col1:
                    st.metric("ATS Score", f"{result['ats_score']}/100")
                with col2:
                    st.metric("Job Match", f"{result['job_match']}%")

                st.divider()

                st.subheader("✅ Matched Skills")
                if result["matched_skills"]:
                    cols = st.columns(3)
                    for i, skill in enumerate(result["matched_skills"]):
                        cols[i % 3].success(skill)

                st.subheader("❌ Missing Skills")
                if result["missing_skills"]:
                    cols = st.columns(3)
                    for i, skill in enumerate(result["missing_skills"]):
                        cols[i % 3].error(skill)

                st.subheader("💡 Suggestions")
                for s in result["suggestions"]:
                    st.info(f"• {s}")

            except Exception as e:
                st.error(f"Error: {e}")