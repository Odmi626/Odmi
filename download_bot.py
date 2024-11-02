import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters.command import Command
from aiogram.types import FSInputFile
import yt_dlp
import os

bot = Bot(token="......")
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("👋 Привіт! Надішліть мені посилання на відео з TikTok або YouTube, і я допоможу тобі завантажити відео.")

@dp.message(F.text.contains("tiktok.com") | F.text.contains("youtube.com") | F.text.contains("youtu.be"))
async def download_video(message: types.Message):
    try:
        url = message.text.strip()
        
        await message.answer("⏳ Починаю завантаження...")
        
        ydl_opts = {
            'format': 'best',
            'outtmpl': 'downloads/%(title)s.%(ext)s'
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
        
        file = FSInputFile(filename)
        await message.answer_video(file, caption="🎥 Ось твоє відео!")
            
        os.remove(filename)
        
    except Exception as e:
        await message.answer(f"❌ Сталася помилка: {str(e)}")

async def main():
    if not os.path.exists('downloads'):
        os.makedirs('downloads')
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
