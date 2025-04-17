from transformers import pipeline

summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
print(summarizer("Hugging Face transformers make NLP simple!", max_length=20, min_length=5, do_sample=False))

def summarize_jd(text):
    return summarizer(text, max_length=120, min_length=30, do_sample=False)[0]["summary_text"]
