from typing import List, Tuple


def format_rag_response(answer: str, sources: List[Tuple[str, str, float]]) -> str:
    source_lines = []
    seen = set()
    for source, text, score in sources:
        if source not in seen:
            seen.add(source)
            preview = text[:120].replace("\n", " ") + "..."
            source_lines.append(f"- [{source}] {preview}")

    sources_block = "\n".join(source_lines)
    return (
        f"{answer}\n\n"
        f"---\n"
        f"Sources used:\n{sources_block}"
    )


def format_error(message: str) -> str:
    return f"Error: {message}\n\nPlease try again or use /help for usage instructions."


def format_help() -> str:
    return (
        "Available commands:\n\n"
        "/ask <your question> — Ask anything from the knowledge base.\n"
        "/help — Show this message.\n\n"
        "Example:\n"
        "  /ask What is rate limiting?"
    )
