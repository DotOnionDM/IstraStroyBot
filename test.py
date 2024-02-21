from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext

from aiogram.types import Message as MSG
from aiogram.types import CallbackQuery as CBQ

import text
from app import bot
from cart import cart
from keyboards import keyboards as kb
from states import States
import json
import io

def def_cart_view(user_id) -> str:
    user_cart = cart.select_all(user_id)

    txt = 'В корзине:\n\n'
    final_sum = 0

    cnt = 0
    for [id_item, shop, art, name, price, count, sm] in user_cart:
        cnt += 1
        txt += f"ID: {id_item}\nМагазин: {shop}\nАртикул: {art}\nНазвание: {name}\nЦена: {price}\nКоличество: {count}\nСтоимость: {sm} руб.\n\n"
        final_sum += int(sm)

    text_order = cart.select_text_order(user_id)
    if (text_order):
        cnt += 1
        txt += text_order + '\n\n'
    else:
        txt += 'Комментарий к заказу отсутствует\n\n'

    txt += f"Общая стоимость всех товаров: {final_sum} руб."
    return (txt, cnt)

def test():
    txt = def_cart_view(675034472)
    with open(f"cart/cart_Netvobed.txt", "w+", encoding="utf-8") as file:
        file.write(txt[0])

if __name__ == '__main__':
    test()