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


def register_admins(dp: Dispatcher):
    dp.register_message_handler(add_admin, commands=['add_admin'], state='*')
    dp.register_message_handler(add_admins_chat, commands=['add_admins_chat'], state='*')
    dp.register_message_handler(ask_prepayment, commands=['prepayment'], state='*')
    dp.register_message_handler(change_prepayment, state=[States.prepayment])
    dp.register_message_handler(ask_sale, commands=['sale'], state='*')
    dp.register_message_handler(change_sale, state=[States.sale])

async def add_admin(msg: MSG):
    with open('admins.json', 'r') as file:
        data = json.load(file)
    data["admin"] = f"{msg.from_user.id}"
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

async def send_order(user_id, username, time_order, time_payment, sum_order, name, phone):
    txt = await cart.def_cart_view(user_id)
    with open(f"cart/cart_{username}.txt", "w+", encoding="utf-8") as file:
        file.write(txt[0])
    order_text = f'Время заявки: {time_order}\n\nВремя оплаты: {time_payment}\n\nСумма: {sum_order}\n\nИмя: {name}\n\nТелефон: {phone}'
    with open('admins.json', 'r') as file:
        data = json.load(file)
    await bot.send_document(data['chat'], open(f"cart/cart_{username}.txt", "rb"),
                            caption=order_text)
    
async def ask_prepayment(user_id):
    with open('admins.json', 'r') as file:
        data = json.load(file)
    if (str(user_id) == data['admin']):
        await States.prepayment.set()
        return await bot.send_message(chat_id=user_id, text='Введите целое число - количество процентов, необходимое для внесения предоплаты.')
    return await bot.send_message(chat_id=user_id, text='Вы не администратор бота', reply_markup=kb.kb_shop_choosing(user_id))

async def change_prepayment(msg: MSG):
    with open('admins.json', 'r') as file:
        data = json.load(file)
    if (str(msg.from_user.id) == data['admin']):
        if msg.text.isdigit() and int(msg.text) > 0:
            cnt = int(msg.text)
        else:
            return await bot.send_message(chat_id=msg.from_user.id, text=text.incorrect_number)
        data["prepayment"] = cnt
        with open('admins.json', 'w') as file:
            json.dump(data, file)
        await msg.answer(f'Размер предоплаты изменен.\n\n{text.choose_shop}', reply_markup=kb.kb_shop_choosing(msg.from_user.id))
        return await States.choose_shop.set()
    await msg.answer(f'Вы не администратор бота.\n\n{text.choose_shop}', reply_markup=kb.kb_shop_choosing(msg.from_user.id))
    return await States.choose_shop.set()

async def ask_sale(user_id):
    with open('admins.json', 'r') as file:
        data = json.load(file)
    if (str(user_id) == data['admin']):
        await States.sale.set()
        return await bot.send_message(chat_id=user_id, text='Введите целое число - размер скидки в процентах.')
    return await bot.send_message(chat_id=user_id, text='Вы не администратор бота', reply_markup=kb.kb_shop_choosing(user_id))

async def change_sale(msg: MSG):
    with open('admins.json', 'r') as file:
        data = json.load(file)
    if (str(msg.from_user.id) == data['admin']):
        if msg.text.isdigit() and int(msg.text) > 0:
            cnt = int(msg.text)
        else:
            return await bot.send_message(chat_id=msg.from_user.id, text=text.incorrect_number)
        data["sale"] = cnt
        with open('admins.json', 'w') as file:
            json.dump(data, file)
        await msg.answer(f'Размер скидки изменен.\n\n{text.choose_shop}', reply_markup=kb.kb_shop_choosing(msg.from_user.id))
        return await States.choose_shop.set()
    await msg.answer(f'Вы не администратор бота.\n\n{text.choose_shop}', reply_markup=kb.kb_shop_choosing(msg.from_user.id))
    return await States.choose_shop.set()