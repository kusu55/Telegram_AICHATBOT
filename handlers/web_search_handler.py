import logging
import json
from serpapi import GoogleSearch
from telegram import Update
from telegram.ext import CallbackContext
from config import WEB_SEARCH_API, GEMINI_API_KEY
import requests


async def web_search(update: Update, context: CallbackContext) -> None:
    """Performs a web search using SerpAPI and provides an AI-generated summary of the results."""

    if not context.args:
        await update.message.reply_text("Please provide a search query after /websearch.")
        return

    query = " ".join(context.args)

    # Step 1: Perform Web Search
    search_params = {
        "q": query,
        "api_key": WEB_SEARCH_API,
        "num": 5  # Fetch top 5 results
    }

    try:
        search = GoogleSearch(search_params)
        data = search.get_dict()
        results = data.get("organic_results", [])

        if not results:
            await update.message.reply_text("No search results found.")
            return

        # Extract top search results
        search_text = "\n".join([f"{res.get('title', 'No Title')}: {res.get('link', 'No Link')}" for res in results])

        # Step 2: Get AI Summary from Gemini API
        summary = await get_ai_summary(query, search_text)

        # Step 3: Send response to the user
        response_message = f"🔍 **Search Summary:**\n\n{summary}\n\n📌 **Top Results:**\n{search_text}"
        await update.message.reply_text(response_message, parse_mode="Markdown")

    except Exception as e:
        logging.error(f"Web search request failed: {e}")
        await update.message.reply_text("❌ Error: Unable to fetch search results.")


async def get_ai_summary(query: str, search_text: str) -> str:
    """Uses the Gemini AI model to generate a summary based on search results."""

    ai_api_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
    headers = {"Content-Type": "application/json"}
    params = {"key": GEMINI_API_KEY}

    prompt = f"Summarize the following search results for the query: '{query}'.\n\n{search_text}"

    payload = json.dumps({"contents": [{"parts": [{"text": prompt}]}]})

    try:
        response = requests.post(ai_api_url, headers=headers, params=params, data=payload)
        response.raise_for_status()
        data = response.json()

        # Extract AI-generated summary
        summary = data.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "")
        return summary if summary else "AI summary not available."

    except Exception as e:
        logging.error(f"AI summary request failed: {e}")
        return "AI summary not available."
