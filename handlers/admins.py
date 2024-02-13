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


def register_admins(dp: Dispatcher):
    dp.register_message_handler(add_admin, commands=['add_admin'])
    dp.register_message_handler(add_admins_chat, commands=['add_admins_chat'])

async def add_admin(msg: MSG):
    data = {"admin": f"{msg.from_user.id}"}
    with open('admins.json', 'w') as file:
        json.dump(data, file)
    await msg.answer('Вы назначены администратором бота.\n\nДля работы с ботом, добавьте его в чат с менеджерами и напишите команду /add_admins_chat.\n\nЭта команда реагирует только на вызов с аккаунта администратора.')

async def add_admins_chat(msg: MSG):
    with open('admins.json', 'r') as file:
        data = json.load(file)
    if (str(msg.from_user.id) == data['admin']):
        data["chat"] = f"{msg.chat.id}"
        with open('admins.json', 'w') as file:
            json.dump(data, file)
        return await msg.answer('Этот чат назначен чатом менеджеров. Сюда будет приходить информация об оплаченных заказах')
    return await msg.answer('Вы не администратор бота')

async def send_order(user_id, username, time_order, time_payment, sum_order, contact):
    txt = await cart.def_cart_view(user_id)
    print(txt)
    file = open(f"cart/cart_{username}.txt", "w+")
    file.write(txt[0])
    file.close()
    order_text = f'Время заявки: {time_order}\n\nВремя оплаты: {time_payment}\n\nСумма: {sum_order}\n\nИмя и телефон:\n{contact}'
    with open('admins.json', 'r') as file:
        data = json.load(file)
    await bot.send_document(data['chat'], open(f"cart/cart_{username}.txt", "rb"),
                            caption=order_text)