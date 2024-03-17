import sqlite3



def create_table(user_id: str) -> None:
    con = sqlite3.connect("data.db")
    cur = con.cursor()
    cur.execute(
        f"CREATE TABLE IF NOT EXISTS '{user_id}' (ID INTEGER PRIMARY KEY AUTOINCREMENT, Shop TEXT, Article INTEGER, Name TEXT, Price INTEGER, PriceSale INTEGER, Count INTEGER, Sum INTEGER, SumSale INTEGER)")
    cur.execute(
        f"CREATE TABLE IF NOT EXISTS 'text_orders' (ID INTEGER PRIMARY KEY AUTOINCREMENT, UserID TEXT, TextOrder TEXT)")
    cur.execute(
        f"CREATE TABLE IF NOT EXISTS 'other_orders' (ID INTEGER PRIMARY KEY AUTOINCREMENT, UserID TEXT, TextOrder TEXT)")
    con.commit()
    con.close()


def add_item(user_id: str, user_data: dict) -> int:
    shop = user_data['shop']
    art = user_data['article']
    name = user_data['name']
    price = user_data['price'] * 100
    saleprice = user_data['saleprice'] * 100
    cnt = user_data['count']
    sm = user_data['sum'] * 100
    salesm = user_data['sumsale'] * 100

    con = sqlite3.connect("data.db")
    cur = con.cursor()
    create_table(user_id)
    was = cur.execute(f"SELECT * FROM '{user_id}' WHERE Article = {art} AND Shop = '{shop}'").fetchone()
    if was:
        con.close()
        return False
    cur.execute(
        f"INSERT INTO '{user_id}' (Shop, Article, Name, Price, PriceSale, Count, Sum, SumSale) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        [shop, art, name, price, saleprice, cnt, sm, salesm])
    con.commit()
    con.close()
    return True


def select_all(user_id: str) -> list:
    con = sqlite3.connect("data.db")
    cur = con.cursor()
    create_table(user_id)
    res = cur.execute(f"SELECT * FROM '{user_id}'").fetchall()
    con.close()
    return res


def item_info(user_id: str, id_item: int):
    con = sqlite3.connect("data.db")
    cur = con.cursor()
    create_table(user_id)
    item = cur.execute(f"SELECT * FROM '{user_id}' WHERE ID = {id_item}").fetchone()
    con.close()
    return item


def change_cnt(user_id: str, user_data: dict) -> None:
    id_item = user_data['id_item']
    new_cnt = user_data['count']
    new_sum = user_data['sum']
    new_sum_sale = user_data['sumsale']
    con = sqlite3.connect("data.db")
    cur = con.cursor()
    create_table(user_id)
    cur.execute(f"UPDATE '{user_id}' SET Count = {new_cnt}, Sum = {new_sum}, SumSale = {new_sum_sale} WHERE ID = {id_item}")
    con.commit()
    con.close()


def change_cnt_by_art(user_id: str, user_data: dict) -> None:
    shop = user_data['shop']
    art = user_data['article']
    new_cnt = user_data['count']
    new_sum = user_data['sum'] * 100
    new_sum_sale = user_data['salesm'] * 100
    con = sqlite3.connect("data.db")
    cur = con.cursor()
    create_table(user_id)
    cur.execute(f"UPDATE '{user_id}' SET Count = {new_cnt}, Sum = {new_sum}, SumSale = {new_sum_sale} WHERE Shop = '{shop}' AND Article = {art}")
    con.commit()
    con.close()


def delete_one_item(user_id: str, id_item: int) -> bool:
    con = sqlite3.connect("data.db")
    cur = con.cursor()
    was = cur.execute(f"SELECT * FROM '{user_id}' WHERE ID = {id_item}").fetchone()
    if was:
        cur.execute(f"DELETE FROM '{user_id}' WHERE ID = {id_item}")
        con.commit()
        con.close()
        return True
    else:
        con.close()
        return False
    
def delete_one_text(user_id: str) -> bool:
    con = sqlite3.connect("data.db")
    cur = con.cursor()
    was = cur.execute(f"SELECT * FROM 'text_orders' WHERE UserID = '{user_id}'").fetchone()
    if was:
        cur.execute(f"DELETE FROM 'text_orders' WHERE UserID = '{user_id}'")
        con.commit()
        con.close()
        return True
    else:
        con.close()
        return False

def delete_one_other(user_id: str) -> bool:
    con = sqlite3.connect("data.db")
    cur = con.cursor()
    was = cur.execute(f"SELECT * FROM 'other_orders' WHERE UserID = '{user_id}'").fetchone()
    if was:
        cur.execute(f"DELETE FROM 'other_orders' WHERE UserID = '{user_id}'")
        con.commit()
        con.close()
        return True
    else:
        con.close()
        return False



def delete_all(user_id: str) -> None:
    con = sqlite3.connect("data.db")
    cur = con.cursor()
    cur.execute(f"DROP TABLE IF EXISTS '{user_id}'")
    cur.execute(f"DELETE FROM 'text_orders' WHERE UserID = {user_id}")
    cur.execute(f"DELETE FROM 'other_orders' WHERE UserID = {user_id}")
    con.commit()
    con.close()

def select_text_order(user_id) -> str:
    con = sqlite3.connect("data.db")
    cur = con.cursor()
    create_table(user_id)
    res = cur.execute(f"SELECT * FROM 'text_orders' WHERE UserID = '{user_id}'").fetchone()
    con.close()
    if res:
        return res[2]
    return res

def select_other_order(user_id) -> str:
    con = sqlite3.connect("data.db")
    cur = con.cursor()
    create_table(user_id)
    res = cur.execute(f"SELECT * FROM 'other_orders' WHERE UserID = '{user_id}'").fetchone()
    con.close()
    if res:
        return res[2]
    return res


async def def_cart_view(user_id) -> str:
    user_cart = select_all(user_id)

    txt = 'В корзине:\n\n'
    final_sum = 0
    final_sale_sum = 0

    cnt = 0
    for [id_item, shop, art, name, price, saleprice, count, sm, salesm] in user_cart:
        cnt += 1
        txt += f"ID: {id_item}\nМагазин: {shop}\nАртикул: {art}\nНазвание: {name}\nЦена в магазине: {price/100} руб.\nЦена со скидкой: {saleprice/100} руб.\nКоличество: {count}\nСтоимость в магазине: {sm/100} руб.\nСтоимость со скидкой: {salesm/100} руб.\n\n"
        final_sum += int(sm)
        final_sale_sum += int(salesm)

    other_order = select_other_order(user_id)
    if (other_order):
        cnt += 1
        txt += other_order + '\n\n'
    else:
        txt += 'Индивидуальный заказ:\n\nОтсутствует.\n\n'

    text_order = select_text_order(user_id)
    if (text_order):
        cnt += 1
        txt += text_order + '\n\n'
    else:
        txt += 'Комментарий к заказу:\n\nОтсутствует.\n\n'

    txt += f"Стоимость в магазине: {final_sum/100} руб.\nСо скидкой Бригадира: {final_sale_sum/100} руб."
    return (txt, cnt, final_sale_sum)

def add_text_order(user_id, text_order) -> None:
    con = sqlite3.connect("data.db")
    cur = con.cursor()
    create_table(user_id)
    prev_text = cur.execute(f"SELECT * FROM 'text_orders' WHERE UserID = '{user_id}'").fetchone()
    if prev_text:
        cur.execute(f"DELETE FROM 'text_orders' WHERE UserID = {user_id}")
        text_order = prev_text[2] + text_order + '\n'
    else:
        text_order = 'Комментарий к заказу:\n' + text_order + '\n'
    cur.execute(
        f"INSERT INTO 'text_orders' (UserID, TextOrder) VALUES (?, ?)", [user_id, text_order])
    con.commit()
    con.close()

def add_other_order(user_id, text_order) -> None:
    con = sqlite3.connect("data.db")
    cur = con.cursor()
    create_table(user_id)
    prev_text = cur.execute(f"SELECT * FROM 'other_orders' WHERE UserID = '{user_id}'").fetchone()
    if prev_text:
        cur.execute(f"DELETE FROM 'other_orders' WHERE UserID = {user_id}")
        text_order = prev_text[2] + text_order + '\n'
    else:
        text_order = 'Индивидуальный заказ:\n' + text_order + '\n'
    cur.execute(
        f"INSERT INTO 'other_orders' (UserID, TextOrder) VALUES (?, ?)", [user_id, text_order])
    con.commit()
    con.close()