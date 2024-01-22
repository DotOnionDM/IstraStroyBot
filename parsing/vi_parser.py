from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time

import text


def parser(article_product):
    options = Options()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)

    try:
        driver.get(f"https://www.vseinstrumenti.ru/search/?what={article_product}")
        time.sleep(3)

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        names = soup.find("h1", class_="typography heading v3 -no-margin")
        price = driver.find_element(By.CSS_SELECTOR, "[data-qa='price-now']")

        names_text = names.text
        change_name = names_text.strip()

        return change_name, price.text
    except:
        driver.quit()
        return None


if __name__ == 'main':
    print(*parser(15888604))