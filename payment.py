import sqlite3
import requests
import json
import config


def create_payment(amount: int) -> tuple:
    code = 404
    i = 0
    while code != 200 and i < 20:
        #url = f"https://enter.tochka.com/uapi/sbp/{config.API_VERSION}/qr-code/merchant/{config.MERCHANT_ID}/{config.ACCOUNT_ID}"
        url = f'https://enter.tochka.com/sandbox/v2/sbp/{config.API_VERSION}/qr-code/merchant/{config.MERCHANT_ID}/{config.ACCOUNT_ID}'
        payload = {
            "Data": {
                "amount": amount * 100,
                "currency": "RUB",
                "paymentPurpose": "Оплата за услуги",
                "qrcType": "02",
                "ttl": 10
            }
        }
        headers = {
            'Authorization': f'Bearer {config.JWT_SANDBOX}'
        }
        response = requests.request("POST", url, headers=headers, json=payload)
        code = response.status_code
        i += 1
    if i >= 20:
        return (None, None)
    info = json.loads(response.text)
    return (info['Data']['qrcId'], info['Data']['payload'])
    

def get_status(qr_id: str) -> str:
    code = 404
    i = 0
    while code != 200 and i < 20:
        #url = f"https://enter.tochka.com/uapi/sbp/{config.API_VERSION}/qr-codes/{qr_id}/payment-status"
        url = f'https://enter.tochka.com/sandbox/v2/sbp/{config.API_VERSION}/qr-codes/{qr_id}/payment-status'
        payload = {}
        headers = {
            'Authorization': f'Bearer {config.JWT_SANDBOX}'
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        code = response.status_code
        i += 1
    if i >= 20:
        return None
    info = json.loads(response.text)
    return info['Data']['paymentList'][0]['status']


def add_qr(user_id: str, qr_id: str) -> None:
    con = sqlite3.connect("data.db")
    cur = con.cursor()
    cur.execute(
        f"CREATE TABLE IF NOT EXISTS payments (ID INTEGER PRIMARY KEY AUTOINCREMENT, qr_id TEXT, user_id TEXT)")
    con.commit()
    cur.execute(f"""
        INSERT INTO payments (qr_id, user_id) VALUES ("{qr_id}", "{user_id}")""")
    con.commit()
    con.close()


def get_qr(user_id: str) -> str:
    con = sqlite3.connect("data.db")
    cur = con.cursor()
    res = cur.execute(f"""
        SELECT qr_id FROM payments WHERE qr_id = "{user_id}" """).fetchone()
    con.close()
    print(res)
    return res


def remove_qr(user_id: str) -> None:
    con = sqlite3.connect("data.db")
    cur = con.cursor()
    cur.execute(f"""
        DELETE FROM payment WHERE user_id = "{user_id}" """)
    con.commit()
    con.close()
 

if __name__ == '__main__':
    pass
    
    