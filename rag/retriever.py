from typing import List, Tuple
import numpy as np
from rag.store import fetch_all
from rag.embedder import embed_query


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.dot(a, b))


def retrieve(query: str, db_path: str, model_name: str, top_k: int) -> List[Tuple[str, str, float]]:
    query_vec = embed_query(query, model_name)
    rows = fetch_all(db_path)

    scored = [
        (source, text, cosine_similarity(query_vec, vec))
        for source, text, vec in rows
    ]
    scored.sort(key=lambda x: x[2], reverse=True)
    return scored[:top_k]
