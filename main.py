import logging
from aiogram import Bot, Dispatcher, executor, types

from config import TOKEN

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.reply('Привет! Я анти-бот. Я буду защищать вашу группу от добавления других ботов.')

@dp.message_handler(content_types=['new_chat_members'])
async def kick_bots(message: types.Message):
    new_members = message.new_chat_members
    for member in new_members:
        logging.info(f"Новый участник: {member.username} (бот: {member.is_bot}, ID: {member.id})")
        if member.is_bot and member.id != bot.id:
            logging.info(f"Попытка удалить бота: {member.username}")
            try:
                await bot.kick_chat_member(chat_id=message.chat.id, user_id=member.id)
                await bot.send_message(chat_id=message.chat.id, text="Бот был удален из группы.")
            except Exception as e:
                logging.error(f"Ошибка при попытке удалить бота: {e}")

async def on_startup(dp):
    logging.info("Бот запускается...")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)