from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer("all-MiniLM-L6-v2")

def match(jd_text, parsed_cvs):
    jd_embedding = model.encode(jd_text, convert_to_tensor=True)
    results = []

    for name, cv_text, skills in parsed_cvs:
        cv_embedding = model.encode(cv_text, convert_to_tensor=True)
        score = float(util.pytorch_cos_sim(jd_embedding, cv_embedding)[0])
        results.append({"name": name, "score": score})

    return results
