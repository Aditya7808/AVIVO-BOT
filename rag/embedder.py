from typing import List
import numpy as np
from sentence_transformers import SentenceTransformer

_model: SentenceTransformer = None


def get_model(model_name: str) -> SentenceTransformer:
    global _model
    if _model is None:
        _model = SentenceTransformer(model_name)
    return _model


def embed_texts(texts: List[str], model_name: str) -> np.ndarray:
    model = get_model(model_name)
    return model.encode(texts, convert_to_numpy=True, normalize_embeddings=True)


def embed_query(query: str, model_name: str) -> np.ndarray:
    return embed_texts([query], model_name)[0]
