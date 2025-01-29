from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import CallbackContext
from database import users_collection
from handlers.chat_handlers import gemini_chat  # Import Gemini chat handler


async def start(update: Update, context: CallbackContext) -> None:
    """Handles user registration."""
    user = update.message.from_user
    chat_id = user.id
    existing_user = users_collection.find_one({"chat_id": chat_id})

    if not existing_user:
        # Request contact before saving to the database
        reply_keyboard = [[KeyboardButton("Share Contact", request_contact=True)]]
        await update.message.reply_text(
            "Please share your phone number or type it manually:",
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True)
        )
        context.user_data["awaiting_phone"] = True
    else:
        await update.message.reply_text(f"Welcome back, {user.first_name}! How can I assist you today?")
        context.user_data["registered"] = True  # Mark user as registered


async def handle_contact(update: Update, context: CallbackContext) -> None:
    """Handles contact saving."""
    user = update.message.from_user
    chat_id = user.id

    if update.message.contact and update.message.contact.user_id == chat_id:
        phone_number = update.message.contact.phone_number

        # Save user info in the database
        users_collection.update_one(
            {"chat_id": chat_id},
            {"$set": {"first_name": user.first_name, "username": user.username, "phone_number": phone_number}},
            upsert=True
        )

        await update.message.reply_text("✅ Thank you! Your phone number has been saved.")

        # Mark user as registered
        context.user_data["registered"] = True
        context.user_data["awaiting_phone"] = False  # Ensure flag is reset

        # Instead of calling gemini_chat, ask the user to send a message
        await update.message.reply_text("✅ Registration complete! You can now start chatting. Just type your message below.")

    else:
        await update.message.reply_text("❌ Error: Please share your own contact information.")


async def handle_text(update: Update, context: CallbackContext) -> None:
    """Handles manually entered phone number or chat after registration."""
    user = update.message.from_user
    chat_id = user.id
    text = update.message.text.strip()

    # Check if the user is entering a phone number
    if context.user_data.get("awaiting_phone"):
        if text.isdigit() and len(text) >= 10:  # Validate minimum length
            # Save the phone number to the database
            users_collection.update_one(
                {"chat_id": chat_id},
                {"$set": {"first_name": user.first_name, "username": user.username, "phone_number": text}},
                upsert=True
            )

            await update.message.reply_text("✅ Thank you! Your phone number has been saved.")

            # Mark user as registered
            context.user_data["awaiting_phone"] = False
            context.user_data["registered"] = True

            await update.message.reply_text("✅ Registration complete! You can now start chatting. Just type your message below.")

        else:
            await update.message.reply_text("❌ Invalid phone number. Please enter a valid one.")

    elif context.user_data.get("registered"):
        # User is registered, forward the message to Gemini AI
        await gemini_chat(update, context)

    else:
        await update.message.reply_text("⚠️ Please register first by sharing your phone number.")
