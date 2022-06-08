
from aiogram import Bot, Dispatcher, executor, types
import logging
import os
import asyncio

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton, ParseMode

from state_db import update_state, get_state
from cust_db import insert_cust_balance, insert_cust_twit, insert_cust_wallet, \
    insert_cust_referral, insert_cust_active, user_exist, get_active, \
    get_balance, get_referral, get_profile, get_referral_num, update_referral_num, insert_cust_ref, get_referred_by
from twitter import check_user, check_follow, find_user

# API_TOKEN = os.getenv('5453415637:AAHw5g_cYJwCyMpmF-ynIoDAbrzqTZlAj5Q')

logging.basicConfig(level=logging.INFO)

bot = Bot(token='5453415637:AAHw5g_cYJwCyMpmF-ynIoDAbrzqTZlAj5Q')

dp = Dispatcher(bot)

twit_user_but = InlineKeyboardButton(
    text="Enter Your twitter username", callback_data='twit')
keyboard_inline = InlineKeyboardMarkup().add(twit_user_but)

Welcomze = """
welcome {} to 

🔰 GeltCoin ~ Airdrop

🎁 Reward Pool: 100000$GELT

🏆 Rating: 🌟🌟🌟🌟🌟



📒 Task (Compulsory)
Please, complete the following task

    1️⃣. First, follow <a href='https://twitter.com/GeltToken'>GiltCoin</a> on twitter.

    2️⃣. send your twitter username (Note you cannot change your twitter username).

    3️⃣. if you have yet to follow, go and follow <a href='https://twitter.com/GeltToken'>GiltCoin</a> on twitter and send in your twitter username again.

    4️⃣. Once above steps are completed successfully, you will be prompted to link your wallet address

    5️⃣. All done now you just have to refer to earn....
 

📚 Info 
    GeltToken is a TRC-20 utility token empowering, facilitating & promoting e-commerce, merchants, exchanges, startups, crypto-mart & retailers accepting crypto for everyday user

"""

accunt = """

🔰 GeltCoin ~ Airdrop

🐦 Twitter Username: {} (Unchangeble)

🏦 Balance: {} $GELT

👥 referrals: {}

Share referral link to more people to get more coins...
"""


def twit_inpun(message: types.Message):
    if get_state(message.chat.id)[-1] == 'twit_input':
        # update_state(message.chat.id, 'normal')
        return True
    else:
        return False


def wallet_inpun(message: types.Message):
    if get_state(message.chat.id)[-1] == 'wallet_input':
        update_state(message.chat.id, 'normal')
        return True
    else:
        return False


def check_balance(message: types.Message):
    if message.text == "🏦Balance":
        update_state(message.chat.id, 'normal')
        return True
    else:
        return False


def check_referral(message: types.Message):
    if message.text == "👥referral link":
        update_state(message.chat.id, 'normal')
        return True
    else:
        return False


def check_profile(message: types.Message):
    if message.text == "👨🏽Profile":
        update_state(message.chat.id, 'normal')
        return True
    else:
        return False


def upd_wallet(message: types.Message):
    if message.text == "⚙️Update wallet":
        update_state(message.chat.id, 'normal')
        return True
    else:
        return False


def u_wallet(message: types.Message):
    if get_state(message.chat.id)[-1] == 'u_wallet':
        update_state(message.chat.id, 'normal')
        return True
    else:
        return False


def daily_coins(message: types.Message):
    if message.text == "🎁Daily Bonus":
        update_state(message.chat.id, 'normal')
        return True
    else:
        return False


def withdraw_(message: types.Message):
    if message.text == "💵Withdraw":
        update_state(message.chat.id, 'normal')
        return True
    else:
        return False


def resume(message: types.Message):
    if message.text == 'resume':
        update_state(message.chat.id, 'normal')
        return True
    else:
        return False


@dp.message_handler(commands='start')
async def welcome(message: types.Message):
    update_state(message.chat.id, 'normal')
    t_name = message.from_user.first_name
    if get_active(message.chat.id) == False:
        ope = message.text.split(" ")
        if len(ope) == 1 or len(ope) > 2:
            insert_cust_ref(message.chat.id, None)
            await message.answer(text=Welcomze.format(t_name), parse_mode='HTML', reply_markup=keyboard_inline)
            
        elif len(ope) == 2:
            try:
                insert_cust_ref(message.chat.id, ope[-1])
                await message.answer(text=Welcomze.format(t_name), parse_mode='HTML', reply_markup=keyboard_inline)
            except:
                insert_cust_ref(message.chat.id, None)
                await message.answer(text=Welcomze.format(t_name), parse_mode='HTML', reply_markup=keyboard_inline)
        else:
            insert_cust_ref(message.chat.id, None)
            await message.answer(text=Welcomze.format(t_name), parse_mode='HTML', reply_markup=keyboard_inline)
    elif get_active(message.chat.id) == True:
        await message.answer("You have already signed up, send resume if to resume your bot processes")


@dp.message_handler(check_balance)
async def balance(msg: types.Message):
    U = get_active(msg.chat.id)
    if U:
        B = get_balance(msg.chat.id)
        if B:
            await msg.answer(f"🏦 Balance: {B} $GELT")
        elif not B:
            await msg.answer("You GOT nothing 🗑")
    elif not U:
        await msg.answer("you have not fully activated your account")


@dp.message_handler(check_referral)
async def balance(msg: types.Message):
    U = get_active(msg.chat.id)
    if U:
        R = get_referral(msg.chat.id)
        if R:
            await msg.answer(f"🔗Link: https://t.me/GeltCoin_bot?start={R}")
        elif not R:
            await msg.answer("You GOT nothing 🗑")
    elif not U:
        await msg.answer("you have not fully activated your account")


@dp.message_handler(check_profile)
async def profile(msg: types.Message):
    U = get_active(msg.chat.id)
    if U:
        P = get_profile(msg.chat.id)
        if P:
            # twitter_username, balance, referrals
            await msg.answer(accunt.format(P[0], P[1], P[2]))
        elif not P:
            await msg.answer("You GOT nothing 🗑")
    elif not U:
        await msg.answer("you have not fully activated your account")


@dp.message_handler(upd_wallet)
async def up_wall(message: types.Message):
    if get_active(message.chat.id) == True:
        await message.answer("Enter your new wallet address or send 'q' or 'Q' to exit...")
        update_state(message.chat.id, 'u_wallet')
    else:
        message.answer("It seems you have not yet signed up")
        update_state(message.chat.id, 'normal')


@dp.message_handler(u_wallet)
async def wall_(message: types.Message):

    if message.text == 'q' or message.text == 'Q':

        await message.answer("exited wallet update")
        update_state(message.chat.id, 'normal')
    elif len(message.text) < 16 or len(message.text) > 36:

        await message.answer(
            "Please enter a valid address.\n(Hint: wallet addresses are usually bigger than 16 characters\npls try again) send 'q' or 'Q' to exit")
        update_state(message.chat.id, 'u_wallet')
    else:

        insert_cust_wallet(message.chat.id, message.text)
        await message.answer("wallet updated successfully....")


@dp.message_handler(daily_coins)  ###################################################
async def daily_c(message: types.Message):
    await message.reply("This feature has not yet been certified pls try again later")


#     U = get_active(message.chat.id)
#     if U:
#         P = get_profile(message.chat.id)
#         if P:
#             # twitter_username, balance, referrals
#             await message.answer()
#         elif not P:
#             await message.answer("You GOT nothing 🗑")
#     elif not U:
#         await message.answer("you have not fully activated your account")

@dp.message_handler(withdraw_)  #####################################################
async def daily_c(message: types.Message):
    await message.reply("This feature has not yet been certified pls try again later")


@dp.message_handler(resume)
async def resome(message: types.Message):
    if get_active(message.chat.id) == True:
        K = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        K = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        K.insert(KeyboardButton("🎁 Daily Bonus"))
        K.insert(KeyboardButton("👥referral link"))
        K.insert(KeyboardButton("🏦Balance"))
        K.insert(KeyboardButton("💵 Withdraw"))
        K.insert(KeyboardButton("⚙️ Update wallet"))
        K.insert(KeyboardButton("👨🏽Profile"))
        await message.reply("Okay, resuming", reply_markup=K)
    else:
        await message.reply("You need to signup first to be able to resume\n\n\nsend /start")


@dp.message_handler(wallet_inpun)
async def wall(message: types.Message):
    update_state(message.chat.id, 'normal')
    if len(message.text) < 16 and len(message.text) > 34:
        await message.answer(
            "Please enter a valid address.\n(Hint: wallet addresses are usually bigger than 16 characters")
        update_state(message.chat.id, 'wallet_input')
    else:
        insert_cust_wallet(message.chat.id, message.text)
        insert_cust_active(message.chat.id)
        K = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        K.insert(KeyboardButton("🎁Daily Bonus"))
        K.insert(KeyboardButton("👥referral link"))
        K.insert(KeyboardButton("🏦Balance"))
        K.insert(KeyboardButton("💵Withdraw"))
        K.insert(KeyboardButton("⚙️Update wallet"))
        K.insert(KeyboardButton("👨🏽Profile"))
        # try:

        try:
            await bot.send_message(get_referred_by(message.chat.id), "➕ New referral added\n🏦Balance + 200")
            insert_cust_referral(get_referred_by(message.chat.id))
            insert_cust_balance(get_referred_by(message.chat.id), 200)
        except:
            pass
        # except:
        #     pass
        # insert_cust_referral()
        await message.answer("wallet successfully linked\nAll done! now you just have to refer to earn", reply_markup=K)


@dp.message_handler(twit_inpun)
async def twit(message: types.Message, call_text=None):
    # await message.delete()
    t = message.text
    if not call_text:
        await bot.delete_message(message.chat.id, message.message_id)
        await bot.delete_message(message.chat.id, message.message_id - 1)
        await bot.delete_message(message.chat.id, message.message_id - 2)
        await message.answer(text=Welcomze.format(message.chat.first_name), parse_mode='HTML')

    I = InlineKeyboardMarkup(row_width=2)
    if call_text:
        screen_name = call_text if call_text[0] != "@" else call_text[1:]
    else:
        screen_name = t if t[0] != "@" else t[1:]

    a = check_user(screen_name=screen_name)
    # await bot.delete_message(message.chat.id, message.message_id - 1)

    if isinstance(a, list):
        update_state(user_id=message.chat.id, state_={"last": "get_user_list"})
        for i in a:
            button = InlineKeyboardButton(
                text="@" + i.get("screen_name"), callback_data=i.get("screen_name"))
            I.insert(button)

        I.insert(InlineKeyboardButton(text="non", callback_data="non"))
        await message.reply("please choose which of this you think is you", reply_markup=I)
        # await bot.delete_message(message.chat.id, message.message_id)

    elif isinstance(a, tuple):
        update_state(user_id=str(message.chat.id),
                     state_={"last": "get_user_tuple"})

        item1 = InlineKeyboardButton("yes", callback_data="yes")
        item2 = InlineKeyboardButton("no", callback_data="no")

        I.insert(item1)
        I.insert(item2)


        doc = f"""
        Is this you?\n
        name: {a[2]}
        handle: {a[1]}
        followers: {a[3]}
        """
        # (i.id_str, i.screen_name, i.name, i.followers_count,)
        # await bot.delete_message(message.chat.id, message.message_id)

        if a[4]:
            await message.answer_photo(a[4], doc, reply_markup=I)
        else:
            await message.answer(doc, reply_markup=I)


        update_state(user_id=message.chat.id, state_=str(
            message.message_id) + " " + a[1] + " " + a[0])
        # await bot.delete_message(message.chat.id, message.message_id)


    elif not a:
        await message.answer("account not found\nplease ensure you type the correct name begining with @")
        update_state(user_id=message.chat.id, state_="twit_input")
        # await bot.delete_message(message.chat.id, message.message_id)



@dp.callback_query_handler()
async def be(call: types.CallbackQuery):
    if call.data == 'twit':
        update_state(call.message.chat.id, 'twit_input')

        # await call.message.delete()
        await call.message.answer("Send your twitter username e.g (@John)")

    elif call.data == "yes" or call.data == "no":
        # await bot.delete_message(call.message.chat.id, call.message.message_id-1)###########
        # await call.answer(text=Welcomze.format(call.message.chat.first_name), )
        await call.message.answer("Please wait, bot is thinking")

        state = get_state(call.message.chat.id)
        if call.data == 'yes':
            if state and len(state[-1].split(" ")) == 3:
                g = state[-1].split(" ")[1]
                # if str(state[0]).startswith(str(call.message.message_id - 1)):
                if True:
                    update_state(user_id=call.message.chat.id, state_='normal')
                    # insert_cust_twit(call.message.chat.id, g)
                    b = check_follow(g)
                    if b:
                        try:
                            insert_cust_twit(call.message.chat.id, g)
                            pass
                        except:
                            await call.message.reply("Sorry, username already in use\nsend in another name")
                            update_state(call.message.chat.id, 'twit_input')
                            # await bot.delete_message(call.message.chat.id, call.message.message_id)

                            # await bot.delete_message(call.message.chat.id, call.message.message_id + 1)

                            return False
                        await call.message.answer(
                            "thank you for following me <a href='https://twitter.com/GeltToken'>@GeltToken</a>\n\n",
                            parse_mode=ParseMode.HTML)
                        update_state(call.message.chat.id, 'wallet_input')
                        await call.message.answer(
                            "send in your wallet address to continue(note: Make sure it is correct unless withdrawal might not be successful)")
                    else:
                        update_state(user_id=call.message.chat.id, state_="twit_input")
                        await call.message.answer(
                            "kindly <a href='https://twitter.com/GeltToken'>click me</a> to follow <a href='https://twitter.com/GeltToken'>@GeltToken</a>\n\n\n##################\n\n\n\n(send in your username again when you are done with following)\n\n\n\n##################",
                            parse_mode=ParseMode.HTML)
        
                    await bot.delete_message(call.message.chat.id, call.message.message_id)
                    
                    # await bot.delete_message(call.message.chat.id, call.message.message_id + 1)
                    # print("7th one")
                    # print("opo", call.message.message_id)

        elif call.data == 'no':
            await call.message.delete()
            # if state:
            g = state[-1]
            # print("This is gg", g)
            if state[1] and len(state[1].split(" ")) == 3:
                # if g.startswith(str(call.message.message_id - 1)):

                g = g.split(" ")[1]
                # print("this is under no screen")
                # print(g)
                go = find_user(g)
                update_state(user_id=call.message.chat.id, state_='normal')
                I = InlineKeyboardMarkup(row_width=1)

                if go:
                    for i in go:
                        # print(i.get("screen_name"))
                        button = InlineKeyboardButton(text="@" + i.get("screen_name"),
                                                      callback_data=i.get("screen_name"))
                        I.insert(button)
                    I.add(InlineKeyboardButton(text="Non of these", callback_data="non"))
                    mm = await call.message.answer("please choose which of this you think is you", reply_markup=I)
                else:
                    update_state(user_id=call.message.chat.id, state_='twit_input')
                    await call.message.answer(
                        "account not found\nplease ensure you type the correct name begining with @")
        # await bot.delete_message(call.message.chat.id, call.message.message_id + 1)
        # print("last one")

    elif call.data == 'non':
        update_state(call.message.chat.id, 'twit_input')
        await call.message.answer("please ensure you type the correct name beginning with @")

    else:
        await bot.delete_message(call.message.chat.id, call.message.message_id)
        # print("this is the last one baba", call.data)
        await twit(call.message, call.data)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=False, )

    # if not user_exist(message.chat.id):
    #     bot_token = message.text.split(" ")
    #     if len(bot_token) < 2:
    #         Ref = None
    #     else:
    #         Ref = get_referral_num(bot_token[1])

    #     if Ref:
    #         update_referral_num(Ref[0], Ref[1] + 1)
    #     else:
    #         pass
