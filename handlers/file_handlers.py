import logging
import base64
import requests
import fitz
from io import BytesIO
from telegram import Update
from telegram.ext import CallbackContext
from database import files_collection
from datetime import datetime
from config import GEMINI_API_KEY
import google.generativeai as genai

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")


async def handle_image(update: Update, context: CallbackContext) -> None:
    """Processes images with Gemini AI."""
    photo = update.message.photo[-1].file_id
    photo_file = await context.bot.get_file(photo)
    file_url = photo_file.file_path

    try:
        response = requests.get(file_url)
        image_bytes = BytesIO(response.content).getvalue()
        image_base64 = base64.b64encode(image_bytes).decode("utf-8")

        gemini_response = model.generate_content([
            {"text": "Describe this image."},
            {"inline_data": {"mime_type": "image/jpeg", "data": image_base64}}
        ])

        response_text = gemini_response.text if gemini_response else "No response from AI."
    except Exception as e:
        logging.error(f"Gemini API Error: {e}")
        response_text = "Error processing the image."

    files_collection.insert_one({
        "chat_id": update.message.chat.id,
        "file_url": file_url,
        "description": response_text,
        "timestamp": datetime.utcnow()
    })

    await update.message.reply_text(f"Image analyzed: {response_text}")


async def handle_file(update: Update, context: CallbackContext) -> None:
    """Handles file uploads and processes them with Gemini AI."""
    document = update.message.document
    file = await document.get_file()
    file_url = file.file_path  # Get the direct Telegram file URL

    extracted_text = ""
    try:
        if document.mime_type == "application/pdf":
            # Fetch file content directly from Telegram
            response = requests.get(file_url)
            doc = fitz.open(stream=response.content, filetype="pdf")
            extracted_text = "\n".join([page.get_text() for page in doc])

        # Generate content with Gemini
        prompt = f"Summarize the contents of this file:\n{extracted_text if extracted_text.strip() else 'No readable text found.'}"
        response = model.generate_content(prompt)
        response_text = response.text
    except Exception as e:
        logging.error(f"Gemini API Error: {e}")
        response_text = "Error processing the file."

    files_collection.insert_one({
        "chat_id": update.message.chat.id,
        "file_url": file_url,
        "description": response_text,
        "timestamp": datetime.utcnow()
    })

    await update.message.reply_text(f"File analyzed: {response_text}")