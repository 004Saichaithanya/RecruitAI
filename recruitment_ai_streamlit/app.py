import streamlit as st
import sqlite3
import bcrypt
import re
from agents import summarizer, parser, notifier, matcher, shortlister

st.set_page_config(layout="wide")

# --- DB Setup ---
def create_users_table():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# --- Utils ---
def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def user_exists(username):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('SELECT 1 FROM users WHERE username = ?', (username,))
    result = c.fetchone()
    conn.close()
    return result is not None

def add_user(username, password):
    if user_exists(username):
        st.error("Username already exists!")
        return False
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    try:
        c.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hash_password(password)))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:  # Catch integrity error for username conflicts
        st.error("Username already exists!")
        return False


def verify_user(username, password):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('SELECT password FROM users WHERE username = ?', (username,))
    result = c.fetchone()
    conn.close()
    return result and bcrypt.checkpw(password.encode('utf-8'), result[0].encode('utf-8'))

def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


# --- App Logic ---
def login_page():
    st.title("🔐 User Authentication")

    menu = ["Login", "Sign Up"]
    choice = st.selectbox("Select Option", menu)

    if choice == "Login":
        username = st.text_input("Username")
        password = st.text_input("Password", type="password",  autocomplete="current-password")

        if st.button("Login"):
            if verify_user(username, password):
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success("✅ Login successful!")
                # st.experimental_rerun()  #REMOVE THIS experimental_rerun() CAUSES LOGIN LOOP
            else:
                st.error("❌ Invalid username or password.")

    elif choice == "Sign Up":
        new_user = st.text_input("New Username")
        new_pass = st.text_input("New Password", type="password",  autocomplete="new-password")

        if st.button("Sign Up"):
            if add_user(new_user, new_pass):
                st.success("✅ Account created!")
                st.info("You can now login from the Login tab.")

def home_page():
    st.title("🧠 Multi-Agent AI Recruitment System")

    # --- JD Upload ---
    st.header("📄 Upload Job Description")
    jd_file = st.file_uploader("Upload JD PDF or Text File", type=["pdf", "txt"])
    jd_summary = ""

    jd_text = ""
    if jd_file is not None:
        try:
            if jd_file.name.endswith(".pdf"):
                jd_text = parser.extract_text(jd_file)
            elif jd_file.name.endswith(".txt"):
                jd_text = parser.extract_txt(jd_file)
            else:
                st.error("❌ Invalid file format. Please upload a PDF or TXT file.")

            st.subheader("Original JD Text")
            st.text_area("JD", jd_text, height=200)

            if st.button("Summarize JD"):
                with st.spinner("Summarizing JD..."):
                    jd_summary = summarizer.summarize_jd(jd_text)
                    st.subheader("Summarized JD")
                    st.success(jd_summary)

        except Exception as e:
            st.error(f"Error processing JD file: {e}")

    # --- CV Upload ---
    st.header("📥 Upload Candidate CVs")
    cv_files = st.file_uploader("Upload one or more PDFs", type=["pdf"], accept_multiple_files=True)

    parsed_cvs = []
    if cv_files:
        for file in cv_files:
            try:
                name, text, skills = parser.parse_cv(file)
                parsed_cvs.append((name, text, skills))
                st.markdown(f"**{name}** - Extracted Skills: `{', '.join(skills)}`")
            except Exception as e:
                st.error(f"Error parsing {file.name}: {e}")

    # --- Matching Logic ---
    if jd_summary and parsed_cvs and st.button("Match Candidates"):
        st.header("🤝 Matching Results")
        matches = matcher.match(jd_summary, parsed_cvs)
        top_candidates = shortlister.shortlist(matches)
        for candidate in top_candidates:
            st.markdown(f"✅ **{candidate['name']}** - Score: {candidate['score']:.2f}")
            st.markdown(f"Skills: `{', '.join(candidate['skills'])}`")

        # --- Notify ---
        emails = st.text_input("Enter comma-separated emails to notify:")
        if st.button("Send Interview Invites"):
            valid_emails = [e.strip() for e in emails.split(",") if is_valid_email(e.strip())]
            if valid_emails:
                notifier.send_emails(valid_emails, top_candidates)
                st.success("✅ Emails sent successfully!")
            else:
                st.error("❌ No valid emails provided.")

    # --- Logout Button ---
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.experimental_rerun()


# --- Main App ---
def main():
    create_users_table()

    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.username = ""

    if st.session_state.logged_in:
        home_page()
    else:
        login_page()

if __name__ == "__main__":
    main()
