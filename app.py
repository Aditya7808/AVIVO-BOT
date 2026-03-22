import logging
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from bot.handlers import handle_ask, handle_help, handle_unknown
from rag.pipeline import build_index
from config import config

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.FileHandler("bot.log"), logging.StreamHandler()],
)
logger = logging.getLogger(__name__)


def main():
    config.validate()

    logger.info("Building RAG index...")
    build_index()
    logger.info("Index ready.")

    app = ApplicationBuilder().token(config.TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("ask", handle_ask))
    app.add_handler(CommandHandler("help", handle_help))
    app.add_handler(MessageHandler(filters.COMMAND, handle_unknown))
    
    # Catch plain text messages and guide the user
    from bot.handlers import handle_text
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    logger.info("Bot is running. Press Ctrl+C to stop.")
    app.run_polling()


if __name__ == "__main__":
    main()
