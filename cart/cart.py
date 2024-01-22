import sqlite3
from states import States


def create_table(user_id: str) -> None:
    con = sqlite3.connect("data.db")
    cur = con.cursor()
    cur.execute(
        f"CREATE TABLE IF NOT EXISTS '{user_id}' (ID INTEGER PRIMARY KEY AUTOINCREMENT, Shop TEXT, Article INTEGER, Name TEXT, Price INTEGER, Count INTEGER, Sum INTEGER)")
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


def change_cnt(user_id: str, user_data: dict) -> None:
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


def delete_one(user_id: str, id_item: int) -> None:
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


def delete_all(user_id: str) -> None:
    con = sqlite3.connect("data.db")
    cur = con.cursor()
    cur.execute(f"DROP TABLE IF EXISTS '{user_id}'")
    con.commit()
    con.close()


async def def_cart_view(user_id) -> str:
    user_cart = select_all(user_id)

    txt = 'В вашей корзине:\n\n'
    final_sum = 0

    for [id_item, shop, art, name, price, count, sm] in user_cart:
        txt += f"ID: {id_item}\nМагазин: {shop}\nАртикул: {art}\nНазвание: {name}\nЦена: {price}\nКоличество: {count}\nСтоимость: {sm}\n\n"
        final_sum += int(sm)

    txt += f"Общая стоимость всех товаров: {final_sum}"
    return txt
