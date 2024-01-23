from aiogram.dispatcher import FSMContext
from keyboards import keyboards as kb
from states import States
from app import bot
from aiogram.types import CallbackQuery as CBQ
from aiogram.types import Message as MSG
from aiogram import Dispatcher
from cart import cart


def register_handlers_cart(dp: Dispatcher):
    dp.register_callback_query_handler(h_cart_view_query, state=States.cart_view_query)
    dp.register_message_handler(h_change_cnt, state=States.change_cnt_id)
    dp.register_message_handler(h_delete_one, state=States.delete_one)
    dp.register_message_handler(h_delete_all, state=States.delete_all)
    dp.register_message_handler(h_payment, state=States.payment)


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
                               text='Введите ID товара, который хотите удалить из корзины.')
        await States.delete_one.set()
    elif data == "del_all":
        await bot.send_message(chat_id=callback.from_user.id,
                               text='Для подтверждения удаления корзины, напишите "Да".')
        await States.delete_all.set()
    else:
        await bot.send_message(chat_id=callback.from_user.id,
                               text='Здесь будет форма для оформления заказа')
        await States.payment.set()


async def h_change_cnt(msg: MSG, state: FSMContext):
    id_item = int(msg.text.strip())
    item = cart.item_info(msg.from_user.id, id_item)
    print(item)
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
    if ret:
        await msg.answer('Товар успешно удален из корзины.')
    else:
        await msg.answer('Товар с этим ID отсутствует в корзине.')
    txt = await cart.def_cart_view(msg.from_user.id)
    await States.cart_view_query.set()
    return await msg.answer(txt, reply_markup=kb.kb_cart())


async def h_delete_all(msg: MSG):
    if msg.text.strip().lower() == 'да':
        cart.delete_all(msg.from_user.id)
    txt = await cart.def_cart_view(msg.from_user.id)
    await States.cart_view_query.set()
    return await msg.answer(txt, reply_markup=kb.kb_cart())


async def h_payment():
    pass

