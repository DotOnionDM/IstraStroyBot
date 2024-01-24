import requests
import json
import config


if __name__ == '__main__':
    url = config.REAL_URL
    sandbox = config.SANDBOX_URL
    payload = {}
    headers = {
        'Authorization': f'Bearer {config.JWT_SANDBOX}'
    }
    response = requests.request("GET", sandbox, headers=headers, data=payload)
    print(response.text)
