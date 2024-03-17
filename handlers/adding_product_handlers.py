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
import json


def register_handlers_add_product(dp: Dispatcher):
    dp.register_message_handler(h_lm_art, state=States.lm_art)
    dp.register_message_handler(h_obi_art, state=States.obi_art)
    dp.register_message_handler(h_petr_art, state=States.petr_art)
    dp.register_message_handler(h_vi_art, state=States.vi_art)
    dp.register_message_handler(h_count_msg, state=States.count)
    dp.register_callback_query_handler(h_count_cbq, state=States.count)
    dp.register_message_handler(h_change_count_msg, state=States.change_cnt_cnt)
    dp.register_callback_query_handler(h_change_count_cbq, state=States.change_cnt_cbq)
    dp.register_callback_query_handler(h_not_add_in_cart, state=[States.not_add_in_cart, States.item_was_in_cart])


async def def_ask_count(art, name, price, id, state: FSMContext):
    with open('admins.json', 'r') as file:
        data = json.load(file)
    sale = data['sale']
    saleprice = price * (100 - sale) / 100
    txt = f"{name}\n\nЦена в магазине: {price} руб.\nЦена со скидкой: {saleprice} руб."
    await bot.send_message(chat_id=id, text=txt)
    await state.update_data(article=art)
    await state.update_data(name=name)
    await state.update_data(price=price)
    await state.update_data(saleprice=saleprice)
    await bot.send_message(chat_id=id, text=text.ask_cnt)
    await States.count.set()


async def h_lm_art(msg: MSG, state: FSMContext):
    if (msg.text == '0'):
        await msg.answer(text=text.choose_shop, reply_markup=kb.kb_shop_choosing(msg.from_user.id))
        return await States.choose_shop.set()

    await msg.answer(text.waiting_art)
    article = msg.text
    ret = lm_parser.requests_parser(article)
    if len(ret) == len(text.item_not_find):
        return await msg.answer(text=text.item_not_find2)
        '''
        await msg.answer(text=text.item_not_find, reply_markup=kb.kb_shop_choosing(msg.from_user.id))
        return await States.choose_shop.set()
        '''
    await def_ask_count(article, ret[0], ret[1], msg.from_user.id, state)


async def h_obi_art(msg: MSG, state: FSMContext):
    if (msg.text == '0'):
        await msg.answer(text=text.choose_shop, reply_markup=kb.kb_shop_choosing(msg.from_user.id))
        return await States.choose_shop.set()

    await msg.answer(text.waiting_art)
    article = msg.text
    ret = obi_parser.requests_parser(article)
    if len(ret) == len(text.item_not_find):
        return await msg.answer(text=text.item_not_find2)
        '''
        await msg.answer(text=text.item_not_find, reply_markup=kb.kb_shop_choosing(msg.from_user.id))
        return await States.choose_shop.set()
        '''
    price = int(ret[1].split('.')[0])
    await def_ask_count(article, ret[0], price, msg.from_user.id, state)


async def h_petr_art(msg: MSG, state: FSMContext):
    if (msg.text == '0'):
        await msg.answer(text=text.choose_shop, reply_markup=kb.kb_shop_choosing(msg.from_user.id))
        return await States.choose_shop.set()

    await msg.answer(text.waiting_art)
    article = msg.text
    ret = petr_parser.requests_parser(article)
    if len(ret) == len(text.item_not_find):
        return await msg.answer(text=text.item_not_find2)
        '''
        await msg.answer(text=text.item_not_find, reply_markup=kb.kb_shop_choosing(msg.from_user.id))
        return await States.choose_shop.set()
        '''
    price = int("".join(ret[1].split()[:-1]))
    await def_ask_count(article, ret[0], price, msg.from_user.id, state)


async def h_vi_art(msg: MSG, state: FSMContext):
    if (msg.text == '0'):
        await msg.answer(text=text.choose_shop, reply_markup=kb.kb_shop_choosing(msg.from_user.id))
        return await States.choose_shop.set()

    await msg.answer(text.waiting_art)
    article = msg.text
    ret = vi_parser.parser(article)
    if ret is None:
        return await msg.answer(text=text.item_not_find2)
        '''
        await msg.answer(text=text.item_not_find, reply_markup=kb.kb_shop_choosing(msg.from_user.id))
        return await States.choose_shop.set()
        '''
    price = int("".join(ret[1].split()[:-1]))
    await def_ask_count(article, ret[0], price, msg.from_user.id, state)


async def def_count_msg(t, user_data, chat_id):
    if t.isdigit() and int(t) > 0:
        cnt = int(t)
        sm = int(user_data['price']) * cnt
        salesm = int(user_data['saleprice'] * 100) / 100 * cnt
        return cnt, sm, salesm
    elif t == '0':
        await bot.send_message(chat_id=chat_id, text=text.choose_shop, reply_markup=kb.kb_shop_choosing(chat_id))
        await States.choose_shop.set()
        return None, None, None
    else:
        await bot.send_message(chat_id=chat_id, text=text.incorrect_number)
        return None, None, None


async def h_count_msg(msg: MSG, state: FSMContext):
    t = msg.text
    user_data = await state.get_data()
    [cnt, sm, salesm] = await def_count_msg(t, user_data, msg.from_user.id)
    if cnt is None:
        return
    await state.update_data(count=cnt)
    await state.update_data(sum=sm)
    await state.update_data(sumsale=salesm)
    await msg.answer(text=f'Итоговая стоимость в магазине: {sm} руб.\nИтоговая стоимость со скидкой: {salesm} руб.\n\nДобавить в корзину?',
                     reply_markup=kb.kb_add_in_bag())


async def h_change_count_msg(msg: MSG, state: FSMContext):
    t = msg.text
    user_data = await state.get_data()
    [cnt, sm, salesm] = await def_count_msg(t, user_data, msg.from_user.id)
    if cnt is None:
        return
    await state.update_data(count=cnt)
    await state.update_data(sum=sm)
    await state.update_data(sumsale=salesm)
    await msg.answer(text=f'Итоговая стоимость:\nв магазине: {sm/100} руб.\nсо скидкой: {salesm/100} руб.\n\nСохранить изменения?',
                     reply_markup=kb.kb_add_in_bag())
    await States.change_cnt_cbq.set()


async def h_change_count_cbq(callback: CBQ, state: FSMContext):
    answer = callback.data
    if answer == 'yes':
        user_data = await state.get_data()
        cart.change_cnt(callback.from_user.id, user_data)
        await bot.send_message(chat_id=callback.from_user.id,
                               text='Количество товара изменено.',
                               reply_markup=kb.kb_continue_add())
        await States.continue_choose_shop.set()
    elif answer == 'no':
        await bot.send_message(chat_id=callback.from_user.id,
                               text=text.choose_shop,
                               reply_markup=kb.kb_shop_choosing(callback.from_user.id))
        await States.choose_shop.set()


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
    elif answer == 'no':
        await bot.send_message(chat_id=callback.from_user.id,
                               text=text.choose_shop,
                               reply_markup=kb.kb_shop_choosing(callback.from_user.id))
        await States.choose_shop.set()


async def h_not_add_in_cart(callback: CBQ, state: FSMContext):
    answer = callback.data
    if answer == 'cnt':
        user_data = await state.get_data()
        cart.change_cnt_by_art(callback.from_user.id, user_data)
        await bot.send_message(chat_id=callback.from_user.id,
                               text='Количество товара изменено.',
                               reply_markup=kb.kb_continue_add())
        await States.continue_choose_shop.set()
    elif answer == 'contin':
        await bot.send_message(chat_id=callback.from_user.id,
                               text=text.choose_shop,
                               reply_markup=kb.kb_shop_choosing(callback.from_user.id))
        await States.choose_shop.set()