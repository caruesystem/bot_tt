
from aiogram import Bot, Dispatcher, executor, types
import logging, os, asyncio

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from data_db import update_state, get_state_verify

API_TOKEN = os.getenv('BOT_API')

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)



# @dp.message_handler(commands='start')
# async def alpha(message:types.Message):
#     update_state(message.chat.id, 'verify')
#     await message.reply("Please supply your twitter user name. e.g (@john)")

# def check_state_1(message:types.Message):
#     res = get_state_verify(message.chat.id)
#     if res[-1] == 'verify':
#         return True
#     else:
#         return False

# @dp.message_handler(check_state_1, content_types='text')
# async def beta(message:types.Message):
#     update_state(message.chat.id, 'normal')
#     await message.reply("ready") 

# def check_st(message:types.Message):
#     pass

I = InlineKeyboardMarkup()
for i in ['a','b','c']:
    button = InlineKeyboardButton(text=i, callback_data=i)
    I.insert(button)

@dp.message_handler()
async def a(message:types.Message):
    await message.reply("ok na", reply_markup=I)

@dp.callback_query_handler(text = ['a','b','c'])
async def be(call:types.CallbackQuery):
    if call.data == 'a':
        await call.message.answer("a was selected")
    if call.data == 'b':
        await call.message.answer("b was selected")
    if call.data == 'c':
        await call.message.answer("c was selected")
    await call.answer()

# def check_sub(message:types.Message):
#     if message("""check db if person has linked their phone number"""):
#         if message.text == 'subcribed' or message.text == 'Subcribed' or message.text == 'SUBSCRIBED':
#             return True
#     else:
#         return False

@dp.message_handler(check_sub, content_types='text')
async def sub(message:types.Message):
    if ("""insert salman function here"""):
        pass

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=False)