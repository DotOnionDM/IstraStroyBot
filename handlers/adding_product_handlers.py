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


def register_handlers_add_product(dp: Dispatcher):
    dp.register_message_handler(h_lm_art, state=States.lm_art)
    dp.register_message_handler(h_obi_art, state=States.obi_art)
    dp.register_message_handler(h_petr_art, state=States.petr_art)
    dp.register_message_handler(h_vi_art, state=States.vi_art)
    dp.register_message_handler(h_count_msg, state=States.count)
    dp.register_callback_query_handler(h_count_cbq, state=States.count)
    dp.register_callback_query_handler(h_not_add_in_cart, state=States.not_add_in_cart)


async def def_ask_count(art, name, price, id, state: FSMContext):
    txt = f"{name}\n\n{price} ₽"
    await bot.send_message(chat_id=id, text=txt)
    await state.update_data(article=art)
    await state.update_data(name=name)
    await state.update_data(price=price)
    await bot.send_message(chat_id=id, text=text.ask_cnt)
    await States.count.set()


async def h_lm_art(msg: MSG, state: FSMContext):
    await msg.answer(text.waiting_art)
    article = msg.text
    ret = lm_parser.requests_parser(article)
    if len(ret) == len(text.item_not_find):
        return await msg.answer(text=text.item_not_find)
    await def_ask_count(article, ret[0], ret[1], msg.from_user.id, state)


async def h_obi_art(msg: MSG, state: FSMContext):
    await msg.answer(text.waiting_art)
    article = msg.text
    ret = obi_parser.requests_parser(article)
    if len(ret) == len(text.item_not_find):
        return await msg.answer(text.item_not_find)
    price = int(ret[1].split('.')[0])
    await def_ask_count(article, ret[0], price, msg.from_user.id, state)


async def h_petr_art(msg: MSG, state: FSMContext):
    await msg.answer(text.waiting_art)
    article = msg.text
    ret = petr_parser.requests_parser(article)
    if len(ret) == len(text.item_not_find):
        return await msg.answer(text.item_not_find)
    price = int("".join(ret[1].split()[:-1]))
    await def_ask_count(article, ret[0], price, msg.from_user.id, state)


async def h_vi_art(msg: MSG, state: FSMContext):
    await msg.answer(text.waiting_art)
    article = msg.text
    ret = vi_parser.parser(article)
    if ret is None:
        return await msg.answer(text.item_not_find)
    price = int("".join(ret[1].split()[:-1]))
    await def_ask_count(article, ret[0], price, msg.from_user.id, state)


async def h_count_msg(msg: MSG, state: FSMContext):
    t = msg.text
    if t.isdigit():
        cnt = int(t)
    else:
        return await bot.send_message(chat_id=msg.from_user.id, text='Введите целое число:')
    user_data = await state.get_data()
    money = int(user_data['price']) * cnt
    await state.update_data(count=cnt)
    await state.update_data(sum=money)
    await msg.answer(text=f'Итоговая стоимость: {money}.\n\nДобавить в корзину?',
                     reply_markup=kb.kb_add_in_bag())


async def h_count_cbq(callback: CBQ, state: FSMContext):
    answer = callback.data
    if answer == 'yes':
        user_data = await state.get_data()
        ret = cart.add_item(callback.from_user.id, user_data)
        if ret:
            await bot.send_message(chat_id=callback.from_user.id,
                                   text='Ваш товар добавлен в корзину.',
                                   reply_markup=kb.kb_continue_add())
            await States.continue_choose_shop.set()
        else:
            await bot.send_message(chat_id=callback.from_user.id,
                                   text='Этот товар уже есть в корзине.',
                                   reply_markup=kb.kb_item_was_in_cart())
            await States.item_was_in_cart.set()

    else:
        await bot.send_message(chat_id=callback.from_user.id,
                               text='Выберите следующее действие:',
                               reply_markup=kb.kb_not_add_in_bag())
        await States.not_add_in_cart.set()


async def h_not_add_in_cart(callback: CBQ):
    answer = callback.data
    if answer == 'cnt':
        await bot.send_message(callback.from_user.id, "Добавляем функцию изменения количества товара")
        # await States.change_cnt.set()
    else:
        await bot.send_message(callback.from_user.id, "Добавляем следующие действия")
