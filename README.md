# Dhamaka Bot - Voice-Enabled Hindi Marketing Bot

🚀 **Dhamaka** is an autonomous Telegram bot that generates marketing strategies, images, and videos in Hindi/Hinglish using AI.

## Features

- 🎤 **Hindi Voice Recognition**: Send Hindi voice notes for strategy generation
- 🤖 **AI Strategy Generation**: Google Gemini API for intelligent marketing strategies
- 🖼️ **AI Image Generation**: FLUX image generation via Together AI
- 🎥 **Stock Videos**: Pixabay integration for relevant video content
- 📱 **Telegram Integration**: Seamless Telegram interface

## Quick Start

### Prerequisites

- Python 3.8+
- Telegram Bot Token from @BotFather
- API Keys:
  - Google Gemini
  - Together AI
  - Pixabay

### Installation

```bash
pip install -r requirements.txt
```

### Configuration

Set environment variables:

```bash
export TELEGRAM_TOKEN=your_bot_token
export GOOGLE_API_KEY=your_gemini_key
export TOGETHER_API_KEY=your_together_key
export PIXABAY_KEY=your_pixabay_key
```

### Run Locally

```bash
python main.py
```

### Deploy on Render

1. Push repository to GitHub
2. Create Background Worker on Render
3. Connect GitHub repository
4. Set environment variables
5. Deploy!

## Bot Commands

- `/start` - Start the bot
- `/help` - Get help
- Send text or voice for strategy generation

## Architecture

- **Telegram Bot API**: python-telegram-bot
- **LLM**: Google Gemini 2.0 Flash
- **Image Generation**: Together AI (FLUX)
- **Videos**: Pixabay API
- **Deployment**: Render Background Worker

## License

MIT License - See LICENSE file for details
