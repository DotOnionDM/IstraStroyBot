import logging
from aiogram import executor
from app import dp
from handlers import choosing_shop_handlers, adding_product_handlers, cart_handlers

logging.basicConfig(level='INFO')

choosing_shop_handlers.register_handlers_choosing_shop(dp)
adding_product_handlers.register_handlers_add_product(dp)
cart_handlers.register_handlers_cart(dp)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
