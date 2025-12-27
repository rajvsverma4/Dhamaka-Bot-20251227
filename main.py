import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import google.generativeai as genai
import requests
from tenacity import retry, stop_after_attempt, wait_exponential

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv('TELEGRAM_TOKEN')
GEMINI_API_KEY = os.getenv('GOOGLE_API_KEY')
TOGETHER_API_KEY = os.getenv('TOGETHER_API_KEY')
PIXABAY_KEY = os.getenv('PIXABAY_KEY')

genai.configure(api_key=GEMINI_API_KEY)

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=2, min=2, max=10))
async def generate_strategy(query: str) -> dict:
    """Generate marketing strategy using Gemini API"""
    model = genai.GenerativeModel('gemini-2.0-flash')
    prompt = f"""Generate a Hindi/Hinglish e-commerce marketing strategy for: {query}
    Return JSON with keys: product, market, strategy, keywords, hashtags"""
    response = model.generate_content(prompt)
    return {"strategy": response.text}

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=2, min=2, max=10))
async def generate_image(text: str) -> str:
    """Generate image using FLUX via Together AI"""
    url = "https://api.together.xyz/inference"
    headers = {"Authorization": f"Bearer {TOGETHER_API_KEY}"}
    payload = {
        "model": "black-forest-labs/FLUX.1-schnell",
        "prompt": text,
        "width": 512,
        "height": 512,
        "steps": 4
    }
    response = requests.post(url, json=payload, headers=headers)
    return response.json().get("output", {}).get("choices", [{}])[0].get("image_url", "")

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=2, min=2, max=10))
async def get_video(query: str) -> str:
    """Fetch video from Pixabay"""
    url = f"https://pixabay.com/api/videos/?key={PIXABAY_KEY}&q={query}&per_page=1"
    response = requests.get(url)
    videos = response.json().get("hits", [])
    if videos:
        return videos[0]["videos"]["medium"]["url"]
    return ""

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start command"""
    msg = """🚀 Namaste! Dhamaka mein swagat hain! 🎉
    
    Mujhe aapka business idea bataiye, main generate kar dunga:
    📱 Hinglish Strategy
    🖼️ AI Images (FLUX)
    🎥 Stock Videos
    
    Text ya voice message bhejiye!"""
    await update.message.reply_text(msg)
    logger.info("🤖 Dhamaka Bot LIVE!")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle text messages"""
    try:
        text = update.message.text
        await update.message.reply_text("⏳ Generating strategy...")
        
        result = await generate_strategy(text)
        await update.message.reply_text(f"Strategy: {result['strategy'][:500]}...")
        
        buttons = [
            ["🖼️ Image", "🎥 Video"],
            ["📊 More Details", "🔄 Regenerate"]
        ]
        await update.message.reply_text(
            "What next?",
            reply_markup=types.ReplyKeyboardMarkup(buttons)
        )
    except Exception as e:
        logger.error(f"Error: {e}")
        await update.message.reply_text(f"❌ Error: {str(e)}")

async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle voice messages"""
    try:
        voice_file = await update.message.voice.get_file()
        await voice_file.download_to_drive("voice.ogg")
        
        model = genai.GenerativeModel('gemini-2.0-flash')
        audio_file = genai.upload_file("voice.ogg")
        
        transcription = model.generate_content(
            ["Transcribe this Hindi voice and generate a marketing strategy:", audio_file]
        )
        
        result = await generate_strategy(transcription.text)
        await update.message.reply_text(f"Strategy: {result['strategy'][:500]}...")
    except Exception as e:
        logger.error(f"Voice error: {e}")
        await update.message.reply_text(f"❌ Voice error: {str(e)}")

def main():
    """Start the bot"""
    app = Application.builder().token(BOT_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(MessageHandler(filters.VOICE, handle_voice))
    
    logger.info("🤖 Dhamaka Bot LIVE!")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
