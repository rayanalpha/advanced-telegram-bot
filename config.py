from dotenv import load_dotenv
import os

load_dotenv()

# Telegram API Credentials
API_ID = os.getenv('API_ID')
API_HASH = os.getenv('API_HASH')
BOT_TOKEN = os.getenv('BOT_TOKEN')

# Bot Settings
DOWNLOAD_PATH = './downloads'
ALLOWED_TYPES = ['photo', 'video', 'document', 'audio']
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB

# Create downloads directory if it doesn't exist
if not os.path.exists(DOWNLOAD_PATH):
    os.makedirs(DOWNLOAD_PATH)