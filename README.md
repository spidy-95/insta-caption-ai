# 📸 Photo-to-Caption AI Generator

An AI-powered web app that generates Instagram-style captions from **photos or text descriptions** using the OpenAI API and Streamlit.

Built by **Vaswati Chaudhuri**.

---

## 🚀 Features

- ✍️ **Text mode** – Type a description of your photo and get 5 caption ideas  
- 🖼️ **Image mode** – Upload a JPG/PNG photo and generate captions based on mood, colors, and vibes  
- 🎭 **Multiple styles** – aesthetic, funny, gym, emotional, travel, soft-girl, baddie, minimal  
- 😊 **Emoji-rich captions**  
- 🛡️ **Safety-focused prompts** (no guessing religion, ethnicity, culture, etc.)

---

## 🧰 Tech Stack

| Component | Technology |
|----------|------------|
| Language | Python |
| UI Framework | Streamlit |
| AI Model | OpenAI `gpt-4.1-mini` |
| Image Input | Base64 encoding + OpenAI Responses API |

---

## 📂 Project Structure

```text
INSTA_CAPTION_AI/
├── app.py             # Main Streamlit application
├── requirements.txt   # Python dependencies
└── .venv/             # Local virtual environment (ignored by git)
