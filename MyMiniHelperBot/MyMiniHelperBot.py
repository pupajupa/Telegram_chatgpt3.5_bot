import logging
from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.middlewares.logging import LoggingMiddleware
import openai

# Установка токена для Telegram бота
bot_token = "TG_BOT_TOKEN"

# Установка API-ключа для GPT-3
openai.api_key = "OPEN_API_KEY"

# Инициализация бота и диспетчера
bot = Bot(token=bot_token)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Обработка команды /start
@dp.message_handler(commands=['start'])
async def on_start(message: types.Message):
    await message.answer("Привет! Я бот с встроенным GPT-3. Просто начните писать мне, и я отвечу!")

# Обработка текстовых сообщений
@dp.message_handler(content_types=types.ContentTypes.TEXT)
async def on_text_message(message: types.Message):
    user_message = message.text

    # Отправка сообщения пользователя на GPT-3
    response = openai.Completion.create(
        engine="davinci",
        prompt=user_message,
        max_tokens=250  # Максимальная длина ответа от GPT-3
    )

    bot_message = response.choices[0].text
    await message.answer(bot_message)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
