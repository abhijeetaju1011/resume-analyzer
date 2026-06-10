import streamlit as st
import requests

# Page config
st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="centered"
)

# Title
st.title("📄 AI Resume Analyzer")
st.markdown("Upload your resume and get AI-powered analysis instantly!")
st.divider()

# File upload
uploaded_file = st.file_uploader(
    "Upload Resume (PDF or DOCX)",
    type=["pdf", "docx"]
)

# Job description
job_description = st.text_area(
    "Paste Job Description Here",
    height=200,
    placeholder="Paste the job description you want to match against..."
)

# Analyze button
if st.button("🔍 Analyze Resume", use_container_width=True):

    # Validation
    if not uploaded_file:
        st.error("Please upload a resume file!")
    elif not job_description.strip():
        st.error("Please enter a job description!")
    else:
        with st.spinner("Analyzing your resume with AI... Please wait!"):
            try:
                # Send to FastAPI
                files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
                data = {"job_description": job_description}
                response = requests.post("http://localhost:8000/analyze", files=files, data=data)

                if response.status_code == 200:
                    result = response.json()

                    st.success("✅ Analysis Complete!")
                    st.divider()

                    # Scores
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("ATS Score", f"{result['ats_score']}/100")
                    with col2:
                        st.metric("Job Match", f"{result['job_match']}%")
                    with col3:
                        st.metric("Word Count", result['word_count'])

                    st.divider()

                    # Matched Skills
                    st.subheader("✅ Matched Skills")
                    if result["matched_skills"]:
                        cols = st.columns(3)
                        for i, skill in enumerate(result["matched_skills"]):
                            cols[i % 3].success(skill)
                    else:
                        st.warning("No matched skills found.")

                    # Missing Skills
                    st.subheader("❌ Missing Skills")
                    if result["missing_skills"]:
                        cols = st.columns(3)
                        for i, skill in enumerate(result["missing_skills"]):
                            cols[i % 3].error(skill)
                    else:
                        st.success("No missing skills!")

                    # Suggestions
                    st.subheader("💡 Improvement Suggestions")
                    for suggestion in result["suggestions"]:
                        st.info(f"• {suggestion}")

                    # ATS Feedback
                    st.subheader("📋 ATS Feedback")
                    for feedback in result["ats_feedback"]:
                        st.write(feedback)

                else:
                    st.error(f"Error: {response.json()['detail']}")

            except Exception as e:
                st.error(f"Something went wrong: {e}")