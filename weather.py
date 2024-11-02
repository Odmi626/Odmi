import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message
import asyncio
import requests

# Замените 'YOUR_BOT_TOKEN' на токен вашего бота
API_TOKEN = '.......'

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

@dp.message(Command('start'))
async def send_welcome(message: Message):
    await message.answer("Привіт! Я бот для отримання погоди. Напиши назву міста, щоб дізнатися про поточну погоду.")
@dp.message()
async def get_weather(message: Message):
    city = message.text
    response = requests.get(f"http://wttr.in/{city}?format=3")
    
    if response.status_code == 200:
        await message.answer(response.text)
    else:
        await message.answer("Місто не знайдено. Спробуйте ще раз.")

async def main():
    dp.message.register(send_welcome, Command(commands=["start"]))
    dp.message.register(get_weather)

    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
