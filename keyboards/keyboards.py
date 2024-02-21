from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.dispatcher import FSMContext
from states import States
import json

def check_admin(user_id):
    with open('admins.json', 'r') as file:
        data = json.load(file)
    if (str(user_id) == data['admin']):
        return True
    return False

def kb_shop_choosing(user_id) -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup()
    lm = InlineKeyboardButton(text="Leroy Merlin", callback_data="Leroy Merlin")
    obi = InlineKeyboardButton(text="OBI", callback_data="OBI")
    petr = InlineKeyboardButton(text="Петрович", callback_data="Петрович")
    vi = InlineKeyboardButton(text="ВсеИнструменты", callback_data="ВсеИнструменты")
    cart = InlineKeyboardButton(text="Посмотреть корзину", callback_data="cart")
    text_order = InlineKeyboardButton(text="Добавить комментарий", callback_data="text_order")
    kb.add(lm, obi)
    kb.add(petr, vi)
    kb.add(cart)
    kb.add(text_order)
    if (check_admin(user_id)):
        prepayment = InlineKeyboardButton(text='Изменить размер предоплаты', callback_data='prepayment')
        sale = InlineKeyboardButton(text='Изменить размер скидки', callback_data='sale')
        kb.add(prepayment)
        kb.add(sale)
    return kb


def kb_add_in_bag() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup()
    yes = InlineKeyboardButton(text="Да", callback_data="yes")
    no = InlineKeyboardButton(text="Нет", callback_data="no")
    kb.add(yes, no)
    return kb


async def kb_change_cnt(state: FSMContext) -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup()
    yes = InlineKeyboardButton(text="Да", callback_data="yes")
    no = InlineKeyboardButton(text="Нет", callback_data="no")
    kb.add(yes, no)
    await States.change_cnt.set()
    return kb


def kb_continue_add() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup()
    yes = InlineKeyboardButton(text="Продолжить добавление товаров", callback_data="yes")
    no = InlineKeyboardButton(text="Посмотреть корзину", callback_data="no")
    kb.add(yes)
    kb.add(no)
    return kb


def kb_cart(user_id) -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup()
    continue_btn = InlineKeyboardButton(text="Продолжить добавление товаров", callback_data="continue")
    change_btn = InlineKeyboardButton(text="Изменить количество товара", callback_data="change")
    del_one_btn = InlineKeyboardButton(text="Удалить товар или комментарий", callback_data="del_one")
    del_all_btn = InlineKeyboardButton(text="Очистить корзину", callback_data="del_all")
    order_btn = InlineKeyboardButton(text="Оформить заказ", callback_data="order")
    kb.add(continue_btn)
    kb.add(change_btn)
    kb.add(del_one_btn)
    kb.add(del_all_btn)
    kb.add(order_btn)
    if (check_admin(user_id)):
        prepayment = InlineKeyboardButton(text='Изменить размер предоплаты', callback_data='prepayment')
        sale = InlineKeyboardButton(text='Изменить размер скидки', callback_data='sale')
        kb.add(prepayment)
        kb.add(sale)
    return kb


def kb_not_add_in_bag() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup()
    cnt = InlineKeyboardButton(text="Изменить количество товара", callback_data="cnt")
    other = InlineKeyboardButton(text="Не добавлять этот товар", callback_data="contin")
    kb.add(cnt)
    kb.add(other)
    return kb


def kb_item_was_in_cart() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup()
    cnt = InlineKeyboardButton(text="Изменить количество товара", callback_data="cnt")
    contin = InlineKeyboardButton(text="Продолжить выбор товаров", callback_data="contin")
    kb.add(cnt)
    kb.add(contin)
    return kb


def kb_check_payment() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup()
    check = InlineKeyboardButton(text="Проверить оплату", callback_data="check_payment")
    cancel = InlineKeyboardButton(text="Отменить", callback_data="cancel")
    kb.add(check)
    kb.add(cancel)
    return kb
