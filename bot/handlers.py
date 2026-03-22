import logging
from collections import defaultdict, deque
from telegram import Update
from telegram.ext import ContextTypes
from rag.pipeline import query as rag_query
from bot.formatter import format_rag_response, format_error, format_help
from config import config

logger = logging.getLogger(__name__)

_history: dict = defaultdict(lambda: deque(maxlen=config.MAX_HISTORY))


def _record(user_id: int, role: str, text: str):
    _history[user_id].append({"role": role, "text": text})


async def handle_ask(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if not args:
        await update.message.reply_text("Usage: /ask <your question>")
        return

    query_text = " ".join(args)
    user_id = update.effective_user.id
    _record(user_id, "user", query_text)

    await update.message.reply_text("Searching knowledge base...")

    try:
        result = rag_query(query_text)
        reply = format_rag_response(result.answer, result.sources)
        _record(user_id, "assistant", result.answer)
        await update.message.reply_text(reply)
    except Exception as e:
        logger.exception("RAG query failed")
        await update.message.reply_text(format_error(str(e)))


async def handle_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(format_help())


async def handle_unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Unknown command. Use /help to see available commands.")


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query_text = update.message.text.strip()
    if not query_text:
        return

    user_id = update.effective_user.id
    _record(user_id, "user", query_text)

    await update.message.reply_text("Searching knowledge base...")

    try:
        result = rag_query(query_text)
        reply = format_rag_response(result.answer, result.sources)
        _record(user_id, "assistant", result.answer)
        await update.message.reply_text(reply)
    except Exception as e:
        logger.exception("RAG query failed on plain text")
        await update.message.reply_text(format_error(str(e)))
