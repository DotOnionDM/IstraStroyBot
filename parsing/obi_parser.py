import requests
import json
import text


def requests_parser(article):
    headers = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:120.0) Gecko/20100101 Firefox/120.0"}
    response = requests.get(f"https://autocomplete.diginetica.net/autocomplete?st={article}&apiKey=1F4667UB1V&regionId=%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B0",
                            headers=headers)
    response_text = json.loads(response.text)
    try:
        art = response_text['products'][0]['id']
        if (art != article):
            return text.item_not_find
        name = response_text['products'][0]['name']
        price = response_text['products'][0]['price']
        return name, price
    except Exception:
        return text.item_not_find
