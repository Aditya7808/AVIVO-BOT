from dataclasses import dataclass
from typing import List, Tuple
from rag.chunker import chunk_documents
from rag.embedder import embed_texts
from rag.store import init_db, is_empty, insert_chunks
from rag.retriever import retrieve
from rag.llm import generate_answer
from config import config


@dataclass
class RAGResult:
    answer: str
    sources: List[Tuple[str, str, float]]


def build_index():
    init_db(config.DB_PATH)
    if not is_empty(config.DB_PATH):
        return

    chunks = chunk_documents(config.DOCS_DIR, config.CHUNK_SIZE, config.CHUNK_OVERLAP)
    texts = [c.text for c in chunks]
    sources = [c.source for c in chunks]
    vectors = embed_texts(texts, config.EMBEDDING_MODEL)
    insert_chunks(config.DB_PATH, sources, texts, vectors)


def query(user_query: str) -> RAGResult:
    results = retrieve(user_query, config.DB_PATH, config.EMBEDDING_MODEL, config.TOP_K)
    context_chunks = [text for _, text, _ in results]

    answer = generate_answer(
        query=user_query,
        context_chunks=context_chunks,
        provider=config.LLM_PROVIDER,
        model=config.LLM_MODEL,
        ollama_url=config.OLLAMA_BASE_URL,
        openai_key=config.OPENAI_API_KEY,
    )
    return RAGResult(answer=answer, sources=results)
