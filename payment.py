import requests
import json
import config


if __name__ == '__main__':
    payload = {}
    headers = {
    'Authorization': f'Bearer {config.JWT_TOKEN}'
    }
    url = f"https://enter.tochka.com/uapi/sbp/v1.0/customer/{config.CUSTUMER_CODE}/{config.BANK_CODE}"
    response = requests.request("GET", url, headers=headers, data=payload)
    print(response.text)