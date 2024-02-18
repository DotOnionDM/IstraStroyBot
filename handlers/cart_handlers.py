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

def register_handlers_cart(dp: Dispatcher):
    dp.register_callback_query_handler(h_cart_view_query, state=States.cart_view_query)
    dp.register_message_handler(h_change_cnt, state=States.change_cnt_id)
    dp.register_message_handler(h_delete_one, state=States.delete_one)
    dp.register_message_handler(h_delete_all, state=States.delete_all)
    dp.register_callback_query_handler(h_payment, state=States.payment)
    dp.register_message_handler(h_contact, state=States.contact)


async def h_cart_view_query(callback: CBQ, state: FSMContext):
    data = callback.data
    if data == "continue":
        await bot.send_message(chat_id=callback.from_user.id,
                               text='Выберите магазин:',
                               reply_markup=kb.kb_shop_choosing(callback.from_user.id))
        await States.choose_shop.set()
    elif data == 'prepayment':
        return await admins.ask_prepayment(callback.from_user.id)
    elif data == "change":
        await bot.send_message(chat_id=callback.from_user.id,
                               text='Введите ID товара, количество которого вы хотите изменить.')
        await States.change_cnt_id.set()
    elif data == "del_one":
        await bot.send_message(chat_id=callback.from_user.id,
                               text='Введите ID товара, который хотите удалить из корзины. Для удаления комментария введите 0.')
        await States.delete_one.set()
    elif data == "del_all":
        await bot.send_message(chat_id=callback.from_user.id,
                               text='Для подтверждения удаления корзины, напишите "Да".')
        await States.delete_all.set()
    elif data == "order":
        txt = await cart.def_cart_view(callback.from_user.id)
        cost = int(txt[0].split(" ")[-2])
        if cost == 0:
            '''
            await bot.send_message(chat_id=callback.from_user.id,
                               text='Корзина пустая. Добавьте товары для оформления заказа.',
                               reply_markup=kb.kb_shop_choosing(callback.from_user.id))
            await States.choose_shop.set()
            return
            '''
            cost = 1
            await state.update_data(sum=0)
        time_zone = pytz.timezone('Europe/Moscow')
        time_order = datetime.now(time_zone).strftime("%d.%m.%Y %H:%M:%S")
        await state.update_data(time_order=time_order)
        qr_info = payment.create_payment(cost)
        if qr_info[0] is None:
            await bot.send_message(chat_id=callback.from_user.id,
                               text='Проблема с банком, попробуйте чуть позже. Можете продолжить добавлять товары в корзину.',
                               reply_markup=kb.kb_shop_choosing(callback.from_user.id))
            await States.choose_shop.set()
            return
        payment.add_qr(callback.from_user.id, qr_info[0])
        await bot.send_message(chat_id=callback.from_user.id,
                               text=f'{text.qr}\n {qr_info[1]}', 
                               reply_markup=kb.kb_check_payment())
        await States.payment.set()
    else:
        await bot.send_message(chat_id=callback.from_user.id,
                               text='Выберите магазин:',
                               reply_markup=kb.kb_shop_choosing(callback.from_user.id))
        await States.choose_shop.set()


async def h_change_cnt(msg: MSG, state: FSMContext):
    id_item = int(msg.text.strip())
    item = cart.item_info(msg.from_user.id, id_item)
    if item is None:
        await msg.answer('Товар с этим ID отсутствует в корзине.')
        txt = await cart.def_cart_view(msg.from_user.id)
        await States.cart_view_query.set()
        return await msg.answer(txt[0], reply_markup=kb.kb_cart(msg.from_user.id))
    name = item[3]
    price = item[4]
    await state.update_data(id_item=id_item)
    await state.update_data(shop=item[1])
    await state.update_data(article=item[2])
    await state.update_data(name=name)
    await state.update_data(price=price)
    await msg.answer(f"{name}\n\n{price} ₽\n\nВведите новое количество для этого товара.")
    await States.change_cnt_cnt.set()


async def h_delete_one(msg: MSG):
    id_item = int(msg.text.strip())
    ret = cart.delete_one(msg.from_user.id, id_item)
    txt = await cart.def_cart_view(msg.from_user.id)
    await States.cart_view_query.set()
    if ret:
        return await msg.answer(txt[0], reply_markup=kb.kb_cart(msg.from_user.id))
    else:
        return await msg.answer('Товар с этим ID отсутствует в корзине.', reply_markup=kb.kb_cart(msg.from_user.id))


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
                               text='Выберите магазин:',
                               reply_markup=kb.kb_shop_choosing(callback.from_user.id))
        await States.choose_shop.set()
    elif callback.data == "check_payment":
        qr_id = payment.get_qr(callback.from_user.id)
        status = payment.get_status(qr_id)
        if status == "Accepted":
            time_zone = pytz.timezone('Europe/Moscow')
            time_payment = datetime.now(time_zone).strftime("%d.%m.%Y %H:%M:%S")
            await state.update_data(time_payment=time_payment)
            await bot.send_message(callback.from_user.id, "Платёж принят, для связи введите имя и номер телефона")
            await States.contact.set()
            payment.remove_qr(callback.from_user.id)
        else:
            await bot.send_message(callback.from_user.id, "Платёж пока не принят. Проверьте, оплачен ли заказ, и повторите попытку.",
                                   reply_markup=kb.kb_check_payment())

async def h_contact(msg: MSG, state: FSMContext):
    data = await state.get_data()
    await admins.send_order(msg.from_user.id, msg.from_user.username, data['time_order'],
                            data['time_payment'], data['sum'], msg.text)
    await msg.answer('Ваш заказ передан менеджеру!', reply_markup=kb.kb_shop_choosing(msg.from_user.id))
    cart.delete_all(msg.from_user.id)
    try:
        os.remove('cart/cart_{callback.from_user.username}.txt')
    except FileNotFoundError:
        pass
    await States.choose_shop.set()