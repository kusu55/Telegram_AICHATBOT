import logging
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from handlers.user_handlers import start, handle_contact, handle_text
from handlers.file_handlers import handle_image, handle_file
from handlers.web_search_handler import web_search
from config import BOT_TOKEN

# Logging setup
logging.basicConfig(level=logging.INFO)

# Initialize bot application
app = Application.builder().token(BOT_TOKEN).build()

# Register command handlers
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("websearch", web_search))

# Register message handlers
app.add_handler(MessageHandler(filters.CONTACT, handle_contact))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
app.add_handler(MessageHandler(filters.PHOTO, handle_image))
app.add_handler(MessageHandler(filters.Document.PDF, handle_file))


# Start polling
if __name__ == "__main__":
    print("Bot is running...")
    app.run_polling()
