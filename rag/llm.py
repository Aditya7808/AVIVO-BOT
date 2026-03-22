import hashlib
from typing import List, Dict
import requests


def call_openai(prompt: str, model: str, api_key: str) -> str:
    from openai import OpenAI
    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a precise technical assistant. "
                    "Answer only using the provided context. "
                    "If the context is insufficient, say so clearly."
                ),
            },
            {"role": "user", "content": prompt},
        ],
        max_tokens=512,
        temperature=0.2,
    )
    return response.choices[0].message.content.strip()


def call_ollama(prompt: str, model: str, base_url: str) -> str:
    response = requests.post(
        f"{base_url}/api/generate",
        json={"model": model, "prompt": prompt, "stream": False},
        timeout=60,
    )
    response.raise_for_status()
    return response.json().get("response", "").strip()


_query_cache: Dict[str, str] = {}


def cached_query_key(query: str, context: str) -> str:
    return hashlib.sha256(f"{query}|{context}".encode()).hexdigest()


def generate_answer(
    query: str,
    context_chunks: List[str],
    provider: str,
    model: str,
    ollama_url: str = "",
    openai_key: str = "",
) -> str:
    context = "\n\n".join(context_chunks)
    cache_key = cached_query_key(query, context)

    if cache_key in _query_cache:
        return _query_cache[cache_key]

    prompt = (
        f"Context:\n{context}\n\n"
        f"Question: {query}\n\n"
        f"Answer concisely and accurately based on the context above."
    )

    if provider == "openai":
        answer = call_openai(prompt, model, openai_key)
    elif provider == "ollama":
        answer = call_ollama(prompt, model, ollama_url)
    else:
        raise ValueError(f"Unknown LLM provider: {provider}")

    _query_cache[cache_key] = answer
    return answer
