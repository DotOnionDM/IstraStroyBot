from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher import FSMContext
from states import States

def kb_shop_choosing() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup()
    lm = InlineKeyboardButton(text="Leroy Merlin", callback_data="Leroy Merlin")
    obi = InlineKeyboardButton(text="OBI", callback_data="OBI")
    petr = InlineKeyboardButton(text="Петрович", callback_data="Петрович")
    vi = InlineKeyboardButton(text="ВсеИнструменты", callback_data="ВсеИнструменты")
    cart = InlineKeyboardButton(text="Посмотреть корзину", callback_data="cart")
    kb.add(lm, obi)
    kb.add(petr, vi)
    kb.add(cart)
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


def kb_cart() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup()
    continue_btn = InlineKeyboardButton(text="Продолжить добавление товаров", callback_data="continue")
    change_btn = InlineKeyboardButton(text="Изменить количество товара", callback_data="change")
    del_one_btn = InlineKeyboardButton(text="Удалить товар из корзины", callback_data="del_one")
    del_all_btn = InlineKeyboardButton(text="Очистить корзину", callback_data="del_all")
    order_btn = InlineKeyboardButton(text="Оформить заказ", callback_data="order")
    kb.add(continue_btn, change_btn, del_one_btn, del_all_btn, order_btn)
    return kb


def kb_not_add_in_bag() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup()
    #cnt = InlineKeyboardButton(text="Изменить количество товара", callback_data="cnt")
    other = InlineKeyboardButton(text="Не добавлять этот товар", callback_data="other")
    #kb.add(cnt)
    kb.add(other)
    return kb


def kb_item_was_in_cart() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup()
    cnt = InlineKeyboardButton(text="Изменить количество товара", callback_data="cnt")
    contin = InlineKeyboardButton(text="Продолжить выбор товаров", callback_data="contin")
    kb.add(cnt, contin)
    return kb
