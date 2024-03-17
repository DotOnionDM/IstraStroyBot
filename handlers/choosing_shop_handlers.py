from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext

from aiogram.types import Message as MSG
from aiogram.types import CallbackQuery as CBQ

import text
from app import bot
from cart import cart
from keyboards import keyboards as kb
from states import States
from handlers import admins

import json

def register_handlers_choosing_shop(dp: Dispatcher):
    dp.register_message_handler(h_start, commands=['start'], state='*')
    dp.register_callback_query_handler(h_choose_shop, state=[States.choose_shop])
    dp.register_callback_query_handler(h_continue_choose_shop, state=[States.continue_choose_shop])


# dp.register_message_handler(h_start, commands=['start'], state='*')
async def h_start(msg: MSG):
    await bot.send_message(chat_id=msg.from_id,
                           text=text.start,
                           reply_markup=kb.kb_shop_choosing(msg.from_user.id))
    await States.choose_shop.set()


# dp.register_callback_query_handler(h_choose_shop, state='choose_shop')
async def h_choose_shop(callback: CBQ, state: FSMContext):
    if callback.data == "cart":
        txt = await cart.def_cart_view(callback.from_user.id)
        await States.cart_view_query.set()
        if txt[1] >= 8:
            with open(f"cart/cart_{callback.from_user.username}.txt", "w+", encoding="utf-8") as file:
                file.write(txt[0])
            return await bot.send_document(callback.from_user.id, open(f"cart/cart_{callback.from_user.username}.txt", "rb"),
                                           caption='В вашей корзине много товаров, поэтому отправляем файлом', reply_markup=kb.kb_cart(callback.from_user.id))
        return await bot.send_message(callback.from_user.id, txt[0], reply_markup=kb.kb_cart(callback.from_user.id))
    elif callback.data == 'other_order':
        txt = text.other_order
        await States.other_order.set()
        return await bot.send_message(callback.from_user.id, txt)
    elif callback.data == 'prepayment':
        await States.prepayment.set()
        return await admins.ask_prepayment(callback.from_user.id)
    elif callback.data == 'sale':
        await States.sale.set()
        return await admins.ask_sale(callback.from_user.id)

    shop_name = callback.data
    await state.update_data(shop=shop_name)
    if shop_name == "Leroy Merlin":
        await bot.send_message(chat_id=callback.from_user.id,
                           text=f"{text.shop_1}{shop_name}{text.shop_2}артикул{text.shop_3}")
        await States.lm_art.set()
    elif shop_name == "OBI":
        await bot.send_message(chat_id=callback.from_user.id,
                           text=f"{text.shop_1}{shop_name}{text.shop_2}артикул{text.shop_3}")
        await States.obi_art.set()
    elif shop_name == "Петрович":
        await bot.send_message(chat_id=callback.from_user.id,
                           text=f"{text.shop_1}{shop_name}{text.shop_2}код{text.shop_3}")
        await States.petr_art.set()
    elif shop_name == "ВсеИнструменты":
        await bot.send_message(chat_id=callback.from_user.id,
                           text=f"{text.shop_1}{shop_name}{text.shop_2}код{text.shop_3}")
        await States.vi_art.set()

# dp.register_callback_query_handler(h_continue_choose_shop, state='continue_choose_shop')
async def h_continue_choose_shop(callback: CBQ):
    answer = callback.data
    if answer == 'yes':
        await bot.send_message(chat_id=callback.from_user.id,
                               text=text.choose_shop,
                               reply_markup=kb.kb_shop_choosing(callback.from_user.id))
        await States.choose_shop.set()
    elif answer == 'no':
        await States.cart_view.set()
        txt = await cart.def_cart_view(callback.from_user.id)
        await bot.send_message(callback.from_user.id, text=txt[0], reply_markup=kb.kb_cart(callback.from_user.id))
        await States.cart_view_query.set()
    else:
        await bot.send_message(chat_id=callback.from_user.id,
                               text=text.choose_shop,
                               reply_markup=kb.kb_shop_choosing(callback.from_user.id))
        await States.choose_shop.set()
