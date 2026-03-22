from flask import Flask, request, jsonify, send_from_directory
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from rag.pipeline import build_index, query as rag_query
from config import config

app = Flask(__name__, static_folder="ui")


@app.route("/")
def index():
    return send_from_directory("ui", "index.html")


@app.route("/api/ask", methods=["POST"])
def ask():
    data = request.get_json(force=True)
    user_query = (data.get("query") or "").strip()

    if not user_query:
        return jsonify({"error": "Query cannot be empty."}), 400

    try:
        result = rag_query(user_query)
        sources = [
            {"file": src, "preview": text[:160].replace("\n", " ")}
            for src, text, score in result.sources
        ]
        return jsonify({"answer": result.answer, "sources": sources})
    except Exception as exc:
        return jsonify({"error": str(exc)}), 500


@app.route("/api/health")
def health():
    return jsonify({"status": "ok", "provider": config.LLM_PROVIDER, "model": config.LLM_MODEL, "key_prefix": config.OPENAI_API_KEY[:10]})


if __name__ == "__main__":
    config.validate()
    print(f"DEBUG: API KEY LOADED = {config.OPENAI_API_KEY[:15]}...")
    print("Building index...")
    build_index()
    print("Index ready. Starting UI server at http://localhost:5000")
    app.run(host="0.0.0.0", port=5000, debug=False)
