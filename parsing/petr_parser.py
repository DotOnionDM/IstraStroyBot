from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import time
import text

def requests_parser(article):
    url = f"https://moscow.petrovich.ru/product/{article}/"
    options = Options()
    options.add_argument("--headless")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument(
        "user-agent=Chrome/91.0.4472.124")
    driver = webdriver.Chrome(options=options)
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        'source': '''
            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array;
            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Promise;
            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol;
        '''
    })
    driver.get(url)
    time.sleep(0.5)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    try:
        name = soup.find("h1", {'data-test': 'product-title'})
        price = soup.find('p', {'data-test': 'product-gold-price'})
        n = name.text
        p = price.text
        driver.close()
        driver.quit()
        return n, p
    except:
        driver.close()
        driver.quit()
        return text.item_not_find


if __name__ == 'main':
    print(requests_parser(505442))