from aiogram.types import Message as MSG
from aiogram.types import CallbackQuery as CBQ

from aiogram import Dispatcher
from keyboards import keyboards as kb
from states import States
from cart import cart
import text

def register_handlers_text_order(dp: Dispatcher):
    dp.register_message_handler(h_text_order, state=States.text_order)
    dp.register_message_handler(h_other_order, state=States.other_order)


async def h_text_order(msg: MSG):
    if (msg.text.strip() == '0'):
        await States.choose_shop.set()
        return await msg.answer(text.choose_shop, reply_markup=kb.kb_shop_choosing(msg.from_user.id))
    cart.add_text_order(msg.from_user.id, msg.text)
    await States.choose_shop.set()
    await msg.answer('Комментарий успешно добавлен.', reply_markup=kb.kb_shop_choosing(msg.from_user.id))

async def h_other_order(msg: MSG):
    if (msg.text.strip() == '0'):
        await States.choose_shop.set()
        return await msg.answer(text.choose_shop, reply_markup=kb.kb_shop_choosing(msg.from_user.id))
    cart.add_other_order(msg.from_user.id, msg.text)
    await States.choose_shop.set()
    await msg.answer(text.add_other_order, reply_markup=kb.kb_shop_choosing(msg.from_user.id))