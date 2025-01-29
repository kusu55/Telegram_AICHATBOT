# 🤖 Telegram AI Chatbot

A powerful AI-powered Telegram bot that integrates **Gemini AI**, **MongoDB**, and **SerpAPI** to provide **chat responses, image & file analysis, and web search capabilities**. 🚀

## 🌟 Features
✅ **User Registration** – Stores user details (name, username, chat ID, phone number) in MongoDB.  
✅ **Gemini AI Chat** – AI-powered chatbot using Google Gemini API.  
✅ **Image & File Analysis** – Describes images and extracts content from PDFs.  
✅ **Web Search** – Fetches search results with AI summary using SerpAPI.  
✅ **Chat History Logging** – Saves full chat history in MongoDB.   

## 📌 Tech Stack
- **Python** (asyncio, requests, pymongo, python-telegram-bot)
- **Google Gemini AI API** (for intelligent responses)
- **MongoDB** (for storing user data & chat history)
- **Telegram Bot API** (for handling user interactions)
- **SerpAPI** (for web search)
- **PyMuPDF (fitz)** (for PDF file processing)

# 🔥 Usage  
## 📌 Commands & Functionalities  

| Command            | Description                                      |
|--------------------|--------------------------------------------------|
| `/start`          | Registers the user and stores details in MongoDB. |
| **Chat with AI**  | Send a message, and Gemini AI will generate a response. |
| **Upload Image**  | Sends a detailed analysis of the image.          |
| **Upload PDF File** | Extracts text and provides a summary.           |
| `/websearch <query>` | Fetches search results from SerpAPI.           |

---

## 👥 Contribution Guide  

🔹 **Fork the repository**  
🔹 **Create a new branch:** `git checkout -b feature-xyz`  
🔹 **Commit your changes:** `git commit -m "Add feature xyz"`  
🔹 **Push the branch:** `git push origin feature-xyz`  
🔹 **Create a pull request (PR)**  


