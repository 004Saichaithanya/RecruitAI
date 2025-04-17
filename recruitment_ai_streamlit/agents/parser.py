import fitz  # PyMuPDF

def extract_text(file):
    if file.type == "application/pdf":
        doc = fitz.open(stream=file.read(), filetype="pdf")
        return "".join([page.get_text() for page in doc])
    else:
        return file.read().decode()

def parse_cv(file):
    text = extract_text(file)
    name = file.name
    skills = extract_skills(text)
    return name, text, skills

def extract_skills(text):
    # Dummy example - replace with NLP-based keyword extractor
    keywords = ["python", "java", "sql", "machine learning", "react", "aws"]
    return [word for word in keywords if word.lower() in text.lower()]
