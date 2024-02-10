import logging
import config
import requests
from aiogram import executor
from app import dp
from handlers import choosing_shop_handlers, adding_product_handlers, cart_handlers

logging.basicConfig(level='INFO')

choosing_shop_handlers.register_handlers_choosing_shop(dp)
adding_product_handlers.register_handlers_add_product(dp)
cart_handlers.register_handlers_cart(dp)


if __name__ == "__main__":
    '''payload = {}
    headers = {
        'Authorization': f'Bearer {config.JWT_TOKEN}'
    }
    url = f"https://enter.tochka.com/uapi/sbp/v1.0/customer/{config.CUSTUMER_CODE}/{config.BANK_CODE}"
    response = requests.request("GET", url, headers=headers, data=payload)
    print(response.text)'''
    executor.start_polling(dp, skip_updates=True)
