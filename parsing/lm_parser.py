from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import json
from bs4 import BeautifulSoup
import time
import requests
import text


def update_cookies():
    url = 'https://leroymerlin.ru/shop/'
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
    time.sleep(1)
    jsid = driver.get_cookie("qrator_jsid")['value']
    jsr = driver.get_cookie("qrator_jsr")['value']
    cookies = {"qrator_jsid": jsid, "qrator_jsr": jsr}
    with open("parsing/cookies_LM.json", "w") as file:
        file.write(json.dumps(cookies))
    driver.close()
    driver.quit()


def requests_parser(article):
    time.sleep(2)

    with open("parsing/cookies_LM.json", "r") as file:
        cookies = json.loads(file.read())
    headers = {"User-Agent": "Chrome/116.0.5845.686 YaBrowser/23.9.5.686 Yowser/2.5 Safari/537.36"}
    response = requests.get(f"https://leroymerlin.ru/search/?q={article}", headers=headers, cookies=cookies)

    if response.status_code != 200:
        update_cookies()
        return requests_parser(article)

    soup = BeautifulSoup(response.text, 'html.parser')
    name = soup.find("span", class_="t9jup0e_plp p16wqyak_plp")
    price = soup.find("span", class_="mvc4syb_plp sncjxni_plp bf9hkrt_plp")

    if name is None:
        name = soup.find("a", attrs={"data-qa": "product-name"})
    if price is None:
        price = soup.find("span", attrs={"data-qa": "new-price-main"})
    if price is None:
        price = soup.find("span", attrs={"data-qa": "primary-price-main"})

    if name is None:
        return text.item_not_find
    if price is None:
        return name.text, 'Цена не найдена. Передайте артикул данного товара менеджеру для улучшения работы бота!'
    
    art = soup.find("span", attrs={"data-qa": "product-article"})
    if (art.text.split()[-1] != article):
        return text.item_not_find

    return name.text, int(price.text.replace("\xa0", ""))


if __name__ == "__main__":
    update_cookies()
    print(requests_parser(87547217))
