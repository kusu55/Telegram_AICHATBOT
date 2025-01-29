import logging
import google.generativeai as genai
import nltk
from telegram import Update
from telegram.ext import CallbackContext
from textblob import TextBlob
from database import chats_collection
from datetime import datetime
from config import GEMINI_API_KEY

# Configure Gemini API
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

nltk.download('punkt')


def analyze_sentiment(text):
    """Analyzes sentiment and returns an emoji."""
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    if polarity > 0:
        return "😊"
    elif polarity < 0:
        return "😞"
    else:
        return "🙂"

async def gemini_chat(update: Update, context: CallbackContext) -> None:
    """Handles user messages with Gemini AI and sentiment analysis."""
    user_message = update.message.text
    chat_id = update.message.chat.id

    try:
        response = model.generate_content(user_message)
        bot_reply = response.text + " " + analyze_sentiment(user_message)

        # Save chat history
        chats_collection.insert_one({
            "chat_id": chat_id,
            "user_message": user_message,
            "bot_reply": bot_reply,
            "timestamp": datetime.utcnow()
        })

        await update.message.reply_text(bot_reply)
    except Exception as e:
        logging.error(f"Gemini API Error: {e}")
        await update.message.reply_text("Sorry, I couldn't process that request.")
