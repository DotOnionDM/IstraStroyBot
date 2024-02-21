from aiogram.dispatcher import FSMContext
from keyboards import keyboards as kb
from states import States
from app import bot
from aiogram.types import CallbackQuery as CBQ
from aiogram.types import Message as MSG
from aiogram import Dispatcher
from cart import cart
import payment
import text
import os
from datetime import datetime
import pytz
from handlers import admins
import json

def register_handlers_cart(dp: Dispatcher):
    dp.register_callback_query_handler(h_cart_view_query, state=States.cart_view_query)
    dp.register_message_handler(h_change_cnt, state=States.change_cnt_id)
    dp.register_callback_query_handler(h_del_one, state=States.delete_one)
    dp.register_message_handler(h_delete_one_item, state=States.delete_one_item)
    dp.register_message_handler(h_delete_one_text, state=States.delete_one_text)
    dp.register_message_handler(h_delete_one_other, state=States.delete_one_other)
    dp.register_message_handler(h_delete_all, state=States.delete_all)
    dp.register_callback_query_handler(h_payment, state=States.payment)
    dp.register_message_handler(h_contact_name, state=States.contact_name)
    dp.register_message_handler(h_contact_number, state=States.contact_number)


async def h_cart_view_query(callback: CBQ, state: FSMContext):
    data = callback.data
    if data == "continue":
        await bot.send_message(chat_id=callback.from_user.id,
                               text=text.choose_shop,
                               reply_markup=kb.kb_shop_choosing(callback.from_user.id))
        await States.choose_shop.set()
    elif data == 'text_order':
        await States.text_order.set()
        return await bot.send_message(callback.from_user.id, text.text_order)
    elif data == 'prepayment':
        States.prepayment.set()
        return await admins.ask_prepayment(callback.from_user.id)
    elif data == 'sale':
        States.sale.set()
        return await admins.ask_sale(callback.from_user.id)
    elif data == "change":
        await bot.send_message(chat_id=callback.from_user.id,
                               text='Введите ID товара, количество которого вы хотите изменить.\n\nЧтобы вернуться к выбору магазина, введите 0.')
        await States.change_cnt_id.set()
    elif data == "del_one":
        await bot.send_message(chat_id=callback.from_user.id,
                               text='Выберите, что хотите удалить:',
                               reply_markup=kb.kb_del_one())
        await States.delete_one.set()
    elif data == "del_all":
        await bot.send_message(chat_id=callback.from_user.id,
                               text='Для подтверждения удаления корзины, напишите "Да".\n\nЧтобы вернуться к выбору магазина, введите 0.')
        await States.delete_all.set()
    elif data == "order":
        txt = await cart.def_cart_view(callback.from_user.id)
        cost = int(txt[0].split(" ")[-2])
        if cost == 0:
            await state.update_data(sum=0)
            await state.update_data(salesm=0)
        time_zone = pytz.timezone('Europe/Moscow')
        time_order = datetime.now(time_zone).strftime("%d.%m.%Y %H:%M:%S")
        await state.update_data(time_order=time_order)
        if cost == 0:
            await state.update_data(time_payment=time_order)
            await States.contact_name.set()
            return await bot.send_message(callback.from_user.id, "Введите ваше имя:")
        qr_info = payment.create_payment(cost)
        if qr_info[0] is None:
            await bot.send_message(chat_id=callback.from_user.id,
                               text='Проблема с банком, попробуйте чуть позже. Можете продолжить добавлять товары в корзину.',
                               reply_markup=kb.kb_shop_choosing(callback.from_user.id))
            await States.choose_shop.set()
            return
        payment.add_qr(callback.from_user.id, qr_info[0])
        with open('admins.json', 'r') as file:
            data = json.load(file)
        prepayment = data['prepayment']
        await bot.send_message(chat_id=callback.from_user.id,
                               text=f'{text.qr}{prepayment}%\n\n{qr_info[1]}', 
                               reply_markup=kb.kb_check_payment())
        await States.payment.set()
    else:
        await bot.send_message(chat_id=callback.from_user.id,
                               text=text.choose_shop,
                               reply_markup=kb.kb_shop_choosing(callback.from_user.id))
        await States.choose_shop.set()


async def h_change_cnt(msg: MSG, state: FSMContext):
    id_item = int(msg.text.strip())
    if (id_item == 0):
        await States.cart_view_query.set()
        txt = await cart.def_cart_view(msg.from_user.id)
        return await msg.answer(txt[0], reply_markup=kb.kb_cart(msg.from_user.id))
    item = cart.item_info(msg.from_user.id, id_item)
    if item is None:
        await msg.answer('Товар с этим ID отсутствует в корзине.')
        txt = await cart.def_cart_view(msg.from_user.id)
        await States.cart_view_query.set()
        return await msg.answer(txt[0], reply_markup=kb.kb_cart(msg.from_user.id))
    name = item[3]
    price = item[4]
    saleprice = item[5]
    await state.update_data(id_item=id_item)
    await state.update_data(shop=item[1])
    await state.update_data(article=item[2])
    await state.update_data(name=name)
    await state.update_data(price=price)
    await state.update_data(saleprice=saleprice)
    await msg.answer(f"{name}\n\nЦена в магазине: {price/100} руб.\nЦена со скидкой: {saleprice/100} руб.\n\nВведите новое количество для этого товара.")
    await States.change_cnt_cnt.set()


async def h_del_one(cbq: CBQ):
    data = cbq.data
    if data == 'item':
        await States.delete_one_item.set()
        return await bot.send_message(cbq.from_user.id, text='Введите ID товара, который хотите удалить.\n\nЧтобы вернуться к выбору магазина, введите 0.')
    elif data == 'text':
        await States.delete_one_text.set()
        return await bot.send_message(cbq.from_user.id, text='Для подтверждения удаления комментария, напишите "Да".\n\nЧтобы вернуться к выбору магазина, введите 0.')
    elif data == 'other':
        await States.delete_one_other.set()
        return await bot.send_message(cbq.from_user.id, text='Для подтверждения удаления индивидуального заказа, напишите "Да".\n\nЧтобы вернуться к выбору магазина, введите 0.')
    elif data == 'back':
        await States.choose_shop.set()
        return await bot.send_message(cbq.from_user.id, text=text.choose_shop, reply_markup=kb.kb_shop_choosing(cbq.from_user.id))

async def h_delete_one_item(msg: MSG):
    id_item = int(msg.text.strip())
    if (id_item == 0):
        return await msg.answer(text.choose_shop, reply_markup=kb.kb_shop_choosing(msg.from_user.id))
    ret = cart.delete_one_item(msg.from_user.id, id_item)
    txt = await cart.def_cart_view(msg.from_user.id)
    await States.cart_view_query.set()
    if ret:
        return await msg.answer(txt[0], reply_markup=kb.kb_cart(msg.from_user.id))
    else:
        return await msg.answer('Товар с этим ID отсутствует в корзине.', reply_markup=kb.kb_cart(msg.from_user.id))
    
async def h_delete_one_text(msg: MSG):
    if (msg.text.strip() == '0'):
        return await msg.answer(text.choose_shop, reply_markup=kb.kb_shop_choosing(msg.from_user.id))
    if msg.text.strip().lower() == 'да':
        cart.delete_one_text(msg.from_user.id)
    txt = await cart.def_cart_view(msg.from_user.id)
    await States.cart_view_query.set()
    return await msg.answer(txt[0], reply_markup=kb.kb_cart(msg.from_user.id))


async def h_delete_one_other(msg: MSG):
    if (msg.text.strip() == '0'):
        return await msg.answer(text.choose_shop, reply_markup=kb.kb_shop_choosing(msg.from_user.id))
    if msg.text.strip().lower() == 'да':
        cart.delete_one_other(msg.from_user.id)
    txt = await cart.def_cart_view(msg.from_user.id)
    await States.cart_view_query.set()
    return await msg.answer(txt[0], reply_markup=kb.kb_cart(msg.from_user.id))


async def h_delete_all(msg: MSG):
    if msg.text.strip().lower() == 'да':
        try:
            os.remove(f'cart/cart_{msg.from_user.username}.txt')
        except FileNotFoundError:
            pass
        cart.delete_all(msg.from_user.id)
    txt = await cart.def_cart_view(msg.from_user.id)
    await States.cart_view_query.set()
    return await msg.answer(txt[0], reply_markup=kb.kb_cart(msg.from_user.id))


async def h_payment(callback: CBQ, state: FSMContext):
    if callback.data == "cancel":
        payment.remove_qr(callback.from_user.id)
        await bot.send_message(chat_id=callback.from_user.id,
                               text=text.choose_shop,
                               reply_markup=kb.kb_shop_choosing(callback.from_user.id))
        await States.choose_shop.set()
    elif callback.data == "check_payment":
        qr_id = payment.get_qr(callback.from_user.id)
        status = payment.get_status(qr_id)
        if status == "Accepted":
            time_zone = pytz.timezone('Europe/Moscow')
            time_payment = datetime.now(time_zone).strftime("%d.%m.%Y %H:%M:%S")
            await state.update_data(time_payment=time_payment)
            await bot.send_message(callback.from_user.id, "Платёж принят. Введите ваше имя:")
            await States.contact_name.set()
            payment.remove_qr(callback.from_user.id)
        else:
            await bot.send_message(callback.from_user.id, "Платёж пока не принят. Проверьте, оплачен ли заказ, и повторите попытку.",
                                   reply_markup=kb.kb_check_payment())

async def h_contact_name(msg: MSG, state: FSMContext):
    await state.update_data(name=msg.text)
    await msg.answer("Введите номер телефона, начиная с +7:")
    await States.contact_number.set()

async def h_contact_number(msg: MSG, state: FSMContext):
    data = await state.get_data()
    await admins.send_order(msg.from_user.id, msg.from_user.username, data['time_order'],
                            data['time_payment'], data['sum'], data['name'], msg.text)
    await msg.answer('Ваш заказ передан менеджеру!', reply_markup=kb.kb_shop_choosing(msg.from_user.id))
    cart.delete_all(msg.from_user.id)
    try:
        os.remove('cart/cart_{callback.from_user.username}.txt')
    except FileNotFoundError:
        pass
    await States.choose_shop.set()