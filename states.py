from aiogram.dispatcher.filters.state import State, StatesGroup


class States(StatesGroup):
    prepayment = State()
    sale = State()

    choose_shop = State()
    continue_choose_shop = State()

    text_order = State()
    other_order = State()

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

    change_cnt_id = State()
    change_cnt_cnt = State()
    change_cnt_cbq = State()

    delete_one = State()
    delete_one_item = State()
    delete_one_text = State()
    delete_one_other = State()

    delete_all = State()

    payment = State()
    contact_name = State()
    contact_number = State()