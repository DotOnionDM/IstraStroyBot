from aiogram.dispatcher.filters.state import State, StatesGroup


class States(StatesGroup):
    choose_shop = State()
    continue_choose_shop = State()

    lm_art = State()
    obi_art = State()
    petr_art = State()
    vi_art = State()

    count = State()

    add_in_cart = State()
    not_add_in_cart = State()
    item_was_in_cart = State()

    cart_view = State()
    cart_view_query = State()

    change_cnt = State()
    delete_one = State()
    delete_all = State()

    payment = State()
