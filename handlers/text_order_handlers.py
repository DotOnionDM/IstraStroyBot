from aiogram.types import Message as MSG
from aiogram.types import CallbackQuery as CBQ

from parsing import lm_parser, obi_parser, petr_parser, vi_parser
from aiogram.dispatcher import FSMContext
from aiogram import Dispatcher
from keyboards import keyboards as kb
import text
from states import States
from app import bot
from cart import cart


def register_handlers_text_order(dp: Dispatcher):
    dp.register_message_handler(h_text_order, state=States.text_order)


async def h_text_order(msg: MSG):
    cart.add_text_order(msg.from_user.id, msg.text)
    await States.choose_shop.set()
    await msg.answer('Комментарий успешно добавлен.', reply_markup=kb.kb_shop_choosing())