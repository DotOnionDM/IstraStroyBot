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


def register_handlers_cart(dp: Dispatcher):
    dp.register_callback_query_handler(h_cart_view_query, state=States.cart_view_query)
    dp.register_message_handler(h_change_cnt, state=States.change_cnt_id)
    dp.register_message_handler(h_delete_one, state=States.delete_one)
    dp.register_message_handler(h_delete_all, state=States.delete_all)
    dp.register_callback_query_handler(h_payment, state=States.payment)


async def h_cart_view_query(callback: CBQ, state: FSMContext):
    data = callback.data
    if data == "continue":
        await bot.send_message(chat_id=callback.from_user.id,
                               text='Выберите магазин:',
                               reply_markup=kb.kb_shop_choosing())
        await States.choose_shop.set()
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
        cost = int(txt.split(" ")[-1])
        if cost == 0:
            await bot.send_message(chat_id=callback.from_user.id,
                               text='Корзина пустая. Добавьте товары для оформления заказа.',
                               reply_markup=kb.kb_shop_choosing())
            await States.choose_shop.set()
            return
        qr_info = payment.create_payment(cost)
        if qr_info[0] is None:
            await bot.send_message(chat_id=callback.from_user.id,
                               text='Проблема с банком, попробуйте чуть позже. Можете продолжить добавлять товары в корзину.',
                               reply_markup=kb.kb_shop_choosing())
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
                               reply_markup=kb.kb_shop_choosing())
        await States.choose_shop.set()


async def h_change_cnt(msg: MSG, state: FSMContext):
    id_item = int(msg.text.strip())
    item = cart.item_info(msg.from_user.id, id_item)
    if item is None:
        await msg.answer('Товар с этим ID отсутствует в корзине.')
        txt = await cart.def_cart_view(msg.from_user.id)
        await States.cart_view_query.set()
        return await msg.answer(txt, reply_markup=kb.kb_cart())
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
        return await msg.answer(txt, reply_markup=kb.kb_cart())
    else:
        return await msg.answer('Товар с этим ID отсутствует в корзине.', reply_markup=kb.kb_cart())


async def h_delete_all(msg: MSG):
    if msg.text.strip().lower() == 'да':
        cart.delete_all(msg.from_user.id)
    txt = await cart.def_cart_view(msg.from_user.id)
    await States.cart_view_query.set()
    return await msg.answer(txt, reply_markup=kb.kb_cart())


async def h_payment(callback: CBQ):
    if callback.data == "cancel":
        payment.remove_qr(callback.from_user.id)
        await bot.send_message(chat_id=callback.from_user.id,
                               text='Выберите магазин:',
                               reply_markup=kb.kb_shop_choosing())
        await States.choose_shop.set()
    elif callback.data == "check_payment":
        qr_id = payment.get_qr(callback.from_user.id)
        status = payment.get_status(qr_id)
        if status == "Accepted":
            await bot.send_message(callback.from_user.id, "Платёж принят, с вами свяжется менеджер.")
            payment.remove_qr(callback.from_user.id)
            cart.delete_all(callback.from_user.id)
            await bot.send_message(chat_id=callback.from_user.id,
                               text='Выберите магазин:',
                               reply_markup=kb.kb_shop_choosing())
            await States.choose_shop.set()
        else:
            await bot.send_message(callback.from_user.id, "Платёж пока не принят, удостоверьтесь, что оплатили заказ. Если же заказ оплачен, то ожидайте.",
                                   reply_markup=kb.kb_check_payment())

