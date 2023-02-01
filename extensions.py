import requests
import json
from config import values_dict


class APIException(Exception):
    pass


class Converter:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):
        if quote == base:
            raise APIException('Введены одинаковые валюты.')

        if '-' in str(amount):
            raise APIException('Мне жаль, что вы в минусе...')

        try:
            quote_ticker = values_dict[quote]
        except KeyError:
            raise APIException(f'Такой валюты я не знаю. Введите /help для справки')

        try:
            base_ticker = values_dict[base]
        except KeyError:
            raise APIException('Такой валюты я не знаю. Введите /help для справки')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException('Введите количество в цифрах.')

        r = requests.get(
            f"https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}")
        d = json.loads(r.content)[values_dict[base]]
        result = float(d) * float(amount)

        return result
