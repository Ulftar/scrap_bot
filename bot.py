from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
import auth_data

"""Создание объекта бота"""
bot = Bot(token=auth_data.token)
"""Создание объекта диспетчера для управления хэндлерами"""
dp = Dispatcher(bot)


"""Создание функции ответа на команду старт"""
@dp.message_handler(commands='start')
async def start(message: types.Message):
    await message.answer('Hello!')


if __name__ == '__main__':
    executor.start_polling(dp)