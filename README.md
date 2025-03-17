# Advanced Telegram Bot

A powerful Telegram bot built with Python and Telethon library that offers multiple advanced features.

## Features

- 🌐 Text translation between languages
- 📺 YouTube video download
- 📚 Wikipedia search
- 🌤 Weather information
- 📷 Image compression
- 🖼 Sticker creation
- 📊 File information
- 📈 Bot statistics

## Setup Instructions

1. Install required packages:
```bash
pip install -r requirements.txt
```

2. Create a `.env` file in the project root with the following variables:
```
API_ID=your_api_id
API_HASH=your_api_hash
BOT_TOKEN=your_bot_token
WEATHER_API_KEY=your_openweathermap_api_key
```

To get the API credentials:
- Get `API_ID` and `API_HASH` from https://my.telegram.org
- Get `BOT_TOKEN` from [@BotFather](https://t.me/BotFather)
- Get `WEATHER_API_KEY` from [OpenWeatherMap](https://openweathermap.org/api)

3. Run the bot:
```bash
python bot.py
```

## Available Commands

- `/start` - Start the bot and show available commands
- `/help` - Show help message
- `/translate [source] [target] [text]` - Translate text between languages
- `/youtube [url]` - Download YouTube video
- `/wiki [query]` - Search Wikipedia
- `/weather [city]` - Get weather information
- `/stats` - Show bot statistics

## File Handling Features

Send any file to the bot to:
- Get file information
- Compress images
- Create stickers from images
- Delete files

## Examples

1. Translate text:
```
/translate en fa Hello, how are you?
```

2. Download YouTube video:
```
/youtube https://www.youtube.com/watch?v=example
```

3. Search Wikipedia:
```
/wiki Python programming language
```

4. Get weather:
```
/weather London
```

## Notes

- The bot creates a `downloads` directory to temporarily store downloaded files
- Files are automatically deleted after processing
- Maximum file size limit is 50MB
- Supported file types: photos, videos, documents, audio

## Error Handling

The bot includes comprehensive error handling for:
- Invalid commands
- Failed downloads
- API errors
- File processing errors
- Network issues

## Contributing

Feel free to submit issues and enhancement requests!