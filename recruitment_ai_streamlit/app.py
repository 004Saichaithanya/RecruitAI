import streamlit as st
from agents import summarizer,parser,notifier,matcher,shortlister

st.set_page_config(layout="wide")
st.title("🧠 Multi-Agent AI Recruitment System")

# Upload JD
st.header("📄 Upload Job Description")
jd_file = st.file_uploader("Upload JD PDF or Text File", type=["pdf", "txt"])
jd_summary = ""

if jd_file:
    jd_text = parser.extract_text(jd_file)
    st.subheader("Original JD Text")
    st.text_area("JD", jd_text, height=200)
    if st.button("Summarize JD"):
        jd_summary = summarizer.summarize_jd(jd_text)
        st.subheader("Summarized JD")
        st.success(jd_summary)

# Upload CVs
st.header("📥 Upload Candidate CVs")
cv_files = st.file_uploader("Upload one or more PDFs", type=["pdf"], accept_multiple_files=True)

parsed_cvs = []
if cv_files:
    for file in cv_files:
        name, text, skills = parser.parse_cv(file)
        parsed_cvs.append((name, text, skills))
        st.markdown(f"**{name}** - Extracted Skills: `{', '.join(skills)}`")

# Matching
if jd_summary and parsed_cvs and st.button("Match Candidates"):
    st.header("🤝 Matching Results")
    matches = matcher.match(jd_summary, parsed_cvs)
    top_candidates = shortlister.shortlist(matches)
    for candidate in top_candidates:
        st.markdown(f"✅ **{candidate['name']}** - Similarity: {candidate['score']:.2f}")

    # Notify
    emails = st.text_input("Enter comma-separated emails to notify:")
    if st.button("Send Interview Invites"):
        notifier.send_emails(emails.split(','), top_candidates)
        st.success("✅ Emails sent successfully!")
