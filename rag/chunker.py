from typing import List
from dataclasses import dataclass


@dataclass
class Chunk:
    text: str
    source: str
    index: int


def split_text(text: str, chunk_size: int, overlap: int) -> List[str]:
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = start + chunk_size
        chunks.append(" ".join(words[start:end]))
        start += chunk_size - overlap
    return chunks


def chunk_documents(docs_dir: str, chunk_size: int, overlap: int) -> List[Chunk]:
    import os
    chunks = []
    for filename in os.listdir(docs_dir):
        if not filename.endswith((".txt", ".md")):
            continue
        path = os.path.join(docs_dir, filename)
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        texts = split_text(content, chunk_size, overlap)
        for i, text in enumerate(texts):
            chunks.append(Chunk(text=text.strip(), source=filename, index=i))
    return chunks
