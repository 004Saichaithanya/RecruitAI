# requirements: streamlit, transformers, PyMuPDF
import fitz  # PyMuPDF
import streamlit as st
from transformers import pipeline
import json
import re

# Load model once
extractor = pipeline("text2text-generation", model="google/flan-t5-base")

# --- Helper Functions ---

def extract_text(file):
    if file.type == "application/pdf":
        doc = fitz.open(stream=file.read(), filetype="pdf")
        return "".join([page.get_text() for page in doc])
    else:
        return file.read().decode()

def extract_resume_info_with_gpt(text):
    prompt = f"""
    You are an intelligent resume parser.

    Extract the following fields **only** and return them in **strict JSON format**:
    - Name
    - Skills (as a list)
    - Education (as a list)
    - Work Experience (as a list)
    - Projects (as a list)
    - Achievements (as a list)
    - Certifications (as a list)

    Output format:
    {{
    "Name": "",
    "Skills": [],
    "Education": [],
    "Work Experience": [],
    "Projects": [],
    "Achievements": [],
    "Certifications": []
    }}

    Resume:
    {text[:1500]}  # Limit to avoid model overload
    """

    response = extractor(prompt, max_new_tokens=256)[0]['generated_text']
    return response

def clean_json_string(s):
    s = s.strip()
    s = re.sub(r"(?<!\\)'", '"', s)  # Convert single to double quotes
    s = re.sub(r",\s*}", "}", s)     # Remove trailing commas
    s = re.sub(r",\s*]", "]", s)
    return s

def parse_cv(file):
    text = extract_text(file)
    name = file.name
    resume_info_raw = extract_resume_info_with_gpt(text)

    try:
        cleaned = clean_json_string(resume_info_raw)
        resume_info = json.loads(cleaned)
    except json.JSONDecodeError:
        print("❌ JSON Parsing Failed. Raw Output:")
        print(resume_info_raw)
        resume_info = {"raw_output": resume_info_raw}
    return name, text, resume_info