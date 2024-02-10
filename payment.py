import requests
import json
import config


def create_payment(amount):
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
    

def get_status(qr_id):
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

    

if __name__ == '__main__':
    pass
    
    