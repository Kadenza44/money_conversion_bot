import requests
import json
from config import values_key

class MoneyConvertion:

    @staticmethod
    def convertion(text_user):
        if len(text_user) != 3:
            print('Неверное количество параметров')
            return 'Неверное количество параметров'
        quote = text_user[0].lower()
        base = text_user[1].lower()

        if quote == base:
            print(f'Перевод двух одинаковых валют {quote} недопустим')
            return f'Перевод двух одинаковых валют {quote} недопустим'

        try:
            amount = float(text_user[2])
        except ValueError:
            print(f'неверно задано количество ({text_user[2]})')
            return f'неверно задано количество ({text_user[2]})'

        try:
            quote_ticker = values_key[quote]
        except KeyError:
            print(f'Валюты {quote} нет в списке доступных')
            return f'Валюты {quote} нет в списке доступных'

        try:
            base_ticker = values_key[base]
        except KeyError:
            print(f'Валюты {base} нет в списке доступных')
            return f'Валюты {base} нет в списке доступных'

        r = requests.get(f'https://api.exchangeratesapi.io/latest?base={quote_ticker}&symbols={base_ticker}')
        rate = json.loads(r.content)['rates'][base_ticker]
        text = f'Курс {amount} {quote_ticker} к {base_ticker} равен {rate * amount}'
        return text

