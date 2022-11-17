from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from async_main import collect_data
import auth_data

"""Создание объекта бота"""
bot = Bot(token=auth_data.token)
"""Создание объекта диспетчера для управления хэндлерами"""
dp = Dispatcher(bot)


"""Создание функции ответа на команду старт"""
@dp.message_handler(commands='start')
async def start(message: types.Message):
    start_buttons = ['Москва', 'Новосибирск', 'Екатеринбург']
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)

    await message.answer('Выберите город', reply_markup=keyboard)


"""Обработчик кнопки Москва. Декоратор проверяет точное соответствие текста"""
@dp.message_handler(Text(equals='Москва'))
async def moscow_city(message: types.Message):
    await message.answer('Подождите...')
    chat_id = message.chat.id
    await send_data(city_code='2398', chat_id=chat_id)


"""Обработчик кнопки Новосибирск"""
@dp.message_handler(Text(equals='Новосибирск'))
async def nsk_city(message: types.Message):
    await message.answer('Подождите...')
    chat_id = message.chat.id
    await send_data(city_code='2425', chat_id=chat_id)


"""Обработчик кнопки Екатеринбург"""
@dp.message_handler(Text(equals='Екатеринбург'))
async def ekb_city(message: types.Message):
    await message.answer('Подождите...')
    chat_id = message.chat.id
    await  send_data(city_code='1869', chat_id=chat_id)


async def send_data(city_code='2398', chat_id=''):
    file = await collect_data(city_code=city_code)
    await bot.send_document(chat_id=chat_id, document=open(file, 'rb'))


if __name__ == '__main__':
    executor.start_polling(dp)