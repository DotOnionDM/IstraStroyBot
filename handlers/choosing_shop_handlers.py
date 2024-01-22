from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext

from aiogram.types import Message as MSG
from aiogram.types import CallbackQuery as CBQ

import text
from app import bot
from cart import cart
from keyboards import keyboards as kb
from states import States


def register_handlers_choosing_shop(dp: Dispatcher):
    dp.register_message_handler(h_start, commands=['start'], state='*')
    dp.register_callback_query_handler(h_choose_shop, state=[States.choose_shop])
    dp.register_callback_query_handler(h_continue_choose_shop, state=[States.continue_choose_shop])


# dp.register_message_handler(h_start, commands=['start'], state='*')
async def h_start(msg: MSG):
    await bot.send_message(chat_id=msg.from_id,
                           text=text.start,
                           reply_markup=kb.kb_shop_choosing())
    await States.choose_shop.set()


# dp.register_callback_query_handler(h_choose_shop, state='choose_shop')
async def h_choose_shop(callback: CBQ, state: FSMContext):
    if callback.data == "cart":
        txt = await cart.def_cart_view(callback.from_user.id)
        await States.cart_view_query.set()
        return await bot.send_message(callback.from_user.id, txt, reply_markup=kb.kb_cart())

    shop_name = callback.data
    await bot.send_message(chat_id=callback.from_user.id,
                           text=f"{text.shop_1}{shop_name}{text.shop_2}")
    await state.update_data(shop=shop_name)
    if shop_name == "Leroy Merlin":
        await States.lm_art.set()
    elif shop_name == "OBI":
        await States.obi_art.set()
    elif shop_name == "Петрович":
        await States.petr_art.set()
    elif shop_name == "ВсеИнструменты":
        await States.vi_art.set()


# dp.register_callback_query_handler(h_continue_choose_shop, state='continue_choose_shop')
async def h_continue_choose_shop(callback: CBQ):
    answer = callback.data
    if answer == 'yes':
        await bot.send_message(chat_id=callback.from_user.id,
                               text='Выберите магазин:',
                               reply_markup=kb.kb_shop_choosing())
        await States.choose_shop.set()
    else:
        await States.cart_view.set()
        txt = await cart.def_cart_view(callback.from_user.id)
        await bot.send_message(callback.from_user.id, text=txt, reply_markup=kb.kb_cart())
        await States.cart_view_query.set()
