# AI Group Chat & Document Editor

A professional desktop application that combines multi-model AI chat with a rich document editor. Send a single message to multiple AI models simultaneously and get responses from ChatGPT, Claude, DeepSeek, and more — all in one unified interface.

## Features

- **Multi-Model Group Chat**: Simultaneously query 10+ AI models (OpenAI, Claude, DeepSeek, Gemini, Doubao, Kimi, GLM, Qwen, MiniMax, Yuanbao) with a single message
- **Rich Document Editor**: Built-in Word-like editor powered by Quill.js with auto-save support
- **One-Click Export**: Export documents to DOCX format instantly
- **Conversation History**: Manage and revisit previous chat sessions
- **Privacy-First**: All data stored locally — no cloud dependency
- **Cross-Platform**: Available as macOS app, Docker container, or run directly with Python

## Quick Start

```bash
pip install -r requirements.txt
python app.py
```

Then open `http://localhost:5000` in your browser.

## Tech Stack

- Python Flask (Backend)
- Quill.js (Rich Text Editor)
- TinyDB/JSON (Local Database)
- PyInstaller (macOS Packaging)
