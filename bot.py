import os
import time
from datetime import datetime
from telethon import TelegramClient, events, Button
from telethon.tl.types import DocumentAttributeVideo
from googletrans import Translator
from pytube import YouTube
import wikipedia
import requests
from PIL import Image
import io
from config import API_ID, API_HASH, BOT_TOKEN, DOWNLOAD_PATH, ALLOWED_TYPES, MAX_FILE_SIZE

# Initialize the bot
bot = TelegramClient('bot', API_ID, API_HASH).start(bot_token=BOT_TOKEN)
translator = Translator()

# Command handler for /start
@bot.on(events.NewMessage(pattern='/start'))
async def start(event):
    """Handle the /start command"""
    welcome_message = """🤖 **Welcome to Advanced Telegram Bot!**

Available commands:
/help - Show this help message
/translate - Translate text (usage: /translate en fa Hello)
/youtube - Download YouTube video (usage: /youtube URL)
/wiki - Search Wikipedia (usage: /wiki query)
/weather - Get weather info (usage: /weather city)
/sticker - Create sticker from image
/info - Get file information
/compress - Compress image or video
/stats - Show bot statistics

Send any file to get information about it!"""
    
    await event.respond(welcome_message, buttons=[
        [Button.text("📚 Help", resize=True), Button.text("🌐 Translate", resize=True)],
        [Button.text("📺 YouTube", resize=True), Button.text("📝 Wikipedia", resize=True)],
        [Button.text("🌤 Weather", resize=True), Button.text("📊 Stats", resize=True)]
    ])

# Translation handler
@bot.on(events.NewMessage(pattern='/translate'))
async def translate_text(event):
    """Handle text translation"""
    try:
        # Format: /translate source_lang target_lang text
        args = event.text.split(maxsplit=3)
        if len(args) != 4:
            await event.respond("❌ Usage: /translate source_lang target_lang text\nExample: /translate en fa Hello")
            return
        
        _, src, dest, text = args
        result = translator.translate(text, src=src, dest=dest)
        await event.respond(f"🔄 Translation ({src} ➜ {dest}):\n\n{result.text}")
    except Exception as e:
        await event.respond(f"❌ Translation error: {str(e)}")

# YouTube video download handler
@bot.on(events.NewMessage(pattern='/youtube'))
async def youtube_download(event):
    """Handle YouTube video download"""
    try:
        url = event.text.split()[1]
        status_message = await event.respond("⏳ Processing YouTube video...")
        
        yt = YouTube(url)
        stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
        
        if not stream:
            await status_message.edit("❌ No suitable video stream found!")
            return
            
        video_path = os.path.join(DOWNLOAD_PATH, f"{yt.title}.mp4")
        stream.download(output_path=DOWNLOAD_PATH)
        
        await bot.send_file(
            event.chat_id,
            video_path,
            caption=f"📺 **{yt.title}**\n\n👁 Views: {yt.views:,}\n⭐️ Rating: {yt.rating:.1f}",
            supports_streaming=True
        )
        os.remove(video_path)
        await status_message.delete()
        
    except Exception as e:
        await event.respond(f"❌ YouTube download error: {str(e)}")

# Wikipedia search handler
@bot.on(events.NewMessage(pattern='/wiki'))
async def wiki_search(event):
    """Handle Wikipedia search"""
    try:
        query = ' '.join(event.text.split()[1:])
        wikipedia.set_lang('en')
        result = wikipedia.summary(query, sentences=5)
        await event.respond(f"📚 **Wikipedia: {query}**\n\n{result}")
    except Exception as e:
        await event.respond(f"❌ Wikipedia search error: {str(e)}")

# Weather information handler
@bot.on(events.NewMessage(pattern='/weather'))
async def get_weather(event):
    """Handle weather information requests"""
    try:
        city = ' '.join(event.text.split()[1:])
        api_key = os.getenv('WEATHER_API_KEY')
        if not api_key:
            await event.respond("❌ Weather API key not configured!")
            return
            
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        response = requests.get(url)
        data = response.json()
        
        if response.status_code == 200:
            weather_info = f"""🌤 **Weather in {city}**

🌡 Temperature: {data['main']['temp']}°C
💧 Humidity: {data['main']['humidity']}%
🌪 Wind Speed: {data['wind']['speed']} m/s
☁️ Conditions: {data['weather'][0]['description']}"""
            await event.respond(weather_info)
        else:
            await event.respond("❌ City not found or weather service error!")
            
    except Exception as e:
        await event.respond(f"❌ Weather error: {str(e)}")

# File information handler
@bot.on(events.NewMessage(func=lambda e: e.file))
async def handle_files(event):
    """Handle incoming files"""
    try:
        file = event.file
        file_size = file.size / (1024 * 1024)  # Convert to MB
        
        info = f"""📄 **File Information**

📝 Name: {file.name}
📊 Size: {file_size:.2f} MB
🏷 MIME Type: {file.mime_type}
📅 Date: {datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')}"""
        
        await event.respond(info, buttons=[
            [Button.inline("📦 Compress", b"compress"),
             Button.inline("🖼 Create Sticker", b"sticker")],
            [Button.inline("❌ Delete", b"delete")]
        ])
        
    except Exception as e:
        await event.respond(f"❌ File handling error: {str(e)}")

# Callback query handler
@bot.on(events.CallbackQuery())
async def callback_handler(event):
    """Handle button callbacks"""
    try:
        data = event.data.decode()
        message = await event.get_message()
        
        if data == "compress":
            if not message.file:
                await event.answer("❌ No file to compress!")
                return
                
            if message.file.mime_type.startswith('image'):
                # Compress image
                downloaded = await message.download_media(DOWNLOAD_PATH)
                img = Image.open(downloaded)
                compressed_path = os.path.join(DOWNLOAD_PATH, "compressed_" + os.path.basename(downloaded))
                img.save(compressed_path, quality=60, optimize=True)
                
                await bot.send_file(event.chat_id, compressed_path,
                                  caption="🗜 Compressed image")
                os.remove(downloaded)
                os.remove(compressed_path)
                
        elif data == "sticker":
            if not message.file or not message.file.mime_type.startswith('image'):
                await event.answer("❌ Please provide an image!")
                return
                
            downloaded = await message.download_media(DOWNLOAD_PATH)
            await bot.send_file(event.chat_id, downloaded,
                              force_document=False,
                              attributes=[DocumentAttributeVideo(0, 0, 0)])
            os.remove(downloaded)
            
        elif data == "delete":
            await message.delete()
            
    except Exception as e:
        await event.answer(f"❌ Error: {str(e)}")

# Statistics handler
@bot.on(events.NewMessage(pattern='/stats'))
async def show_stats(event):
    """Show bot statistics"""
    stats = f"""📊 **Bot Statistics**

🕒 Uptime: {time.strftime('%H:%M:%S', time.gmtime(time.time() - bot.start_time))}
💾 Downloads: {len(os.listdir(DOWNLOAD_PATH))}
📁 Storage Used: {sum(os.path.getsize(os.path.join(DOWNLOAD_PATH, f)) for f in os.listdir(DOWNLOAD_PATH)) / (1024*1024):.2f} MB"""
    
    await event.respond(stats)

print("Bot is running...")
bot.run_until_disconnected()