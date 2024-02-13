import sqlite3



def create_table(user_id: str) -> None:
    con = sqlite3.connect("data.db")
    cur = con.cursor()
    cur.execute(
        f"CREATE TABLE IF NOT EXISTS '{user_id}' (ID INTEGER PRIMARY KEY AUTOINCREMENT, Shop TEXT, Article INTEGER, Name TEXT, Price INTEGER, Count INTEGER, Sum INTEGER)")
    cur.execute(
        f"CREATE TABLE IF NOT EXISTS 'text_orders' (ID INTEGER PRIMARY KEY AUTOINCREMENT, UserID TEXT, TextOrder TEXT)")
    con.commit()
    con.close()


def add_item(user_id: str, user_data: dict) -> int:
    shop = user_data['shop']
    art = user_data['article']
    name = user_data['name']
    price = user_data['price']
    cnt = user_data['count']
    sm = user_data['sum']

    con = sqlite3.connect("data.db")
    cur = con.cursor()
    create_table(user_id)
    was = cur.execute(f"SELECT * FROM '{user_id}' WHERE Article = {art} AND Shop = '{shop}'").fetchone()
    if was:
        con.close()
        return False
    cur.execute(
        f"INSERT INTO '{user_id}' (Shop, Article, Name, Price, Count, Sum) VALUES (?, ?, ?, ?, ?, ?)",
        [shop, art, name, price, cnt, sm])
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
    con = sqlite3.connect("data.db")
    cur = con.cursor()
    create_table(user_id)
    cur.execute(f"UPDATE '{user_id}' SET Count = {new_cnt}, Sum = {new_sum} WHERE ID = {id_item}")
    con.commit()
    con.close()


def change_cnt_by_art(user_id: str, user_data: dict) -> None:
    shop = user_data['shop']
    art = user_data['article']
    new_cnt = user_data['count']
    new_sum = user_data['sum']
    con = sqlite3.connect("data.db")
    cur = con.cursor()
    create_table(user_id)
    cur.execute(f"UPDATE '{user_id}' SET Count = {new_cnt}, Sum = {new_sum} WHERE Shop = '{shop}' AND Article = {art}")
    con.commit()
    con.close()


def delete_one(user_id: str, id_item: int) -> bool:
    con = sqlite3.connect("data.db")
    cur = con.cursor()
    if id_item == 0:
        table_name = 'text_orders'
        was = cur.execute(f"SELECT * FROM 'text_orders' WHERE UserID = '{user_id}'").fetchone()
        if was:
            cur.execute(f"DELETE FROM 'text_orders' WHERE UserID = '{user_id}'")
            con.commit()
            con.close()
            return True
        else:
            con.close()
            return False

    was = cur.execute(f"SELECT * FROM '{user_id}' WHERE ID = {id_item}").fetchone()
    if was:
        cur.execute(f"DELETE FROM '{user_id}' WHERE ID = {id_item}")
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


async def def_cart_view(user_id) -> str:
    user_cart = select_all(user_id)

    txt = 'В вашей корзине:\n\n'
    final_sum = 0

    for [id_item, shop, art, name, price, count, sm] in user_cart:
        txt += f"ID: {id_item}\nМагазин: {shop}\nАртикул: {art}\nНазвание: {name}\nЦена: {price}\nКоличество: {count}\nСтоимость: {sm}\n\n"
        final_sum += int(sm)

    text_order = select_text_order(user_id)
    if (text_order):
        txt += text_order + '\n\n'

    txt += f"Общая стоимость всех товаров: {final_sum}"
    return txt

def add_text_order(user_id, text_order) -> None:
    con = sqlite3.connect("data.db")
    cur = con.cursor()
    create_table(user_id)
    prev_text = cur.execute(f"SELECT * FROM 'text_orders' WHERE UserID = '{user_id}'").fetchone()
    if prev_text:
        cur.execute(f"DELETE FROM 'text_orders' WHERE UserID = {user_id}")
        text_order = prev_text[2] + text_order + '\n'
    else:
        text_order = 'Комментарий к заказу:\n' + text_order
    cur.execute(
        f"INSERT INTO 'text_orders' (UserID, TextOrder) VALUES (?, ?)", [user_id, text_order])
    con.commit()
    con.close()