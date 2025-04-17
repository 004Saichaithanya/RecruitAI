def shortlist(candidates, top_k=3):
    return sorted(candidates, key=lambda x: x["score"], reverse=True)[:top_k]
