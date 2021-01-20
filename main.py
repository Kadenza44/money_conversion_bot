import telebot
import requests
import json

TOKEN = '1468477683:AAG4p7PuJXtAXfzW2-g8RNxWblHR3Ll6HgA'

bot = telebot.TeleBot(TOKEN)

r = requests.get('https://api.exchangeratesapi.io/latest?base=USD&symbols=RUB')
print(r.content)
print(json.loads(r.content)['rates']['RUB'])

values_key = {'рубль': 'RUB',
              'доллар': 'USD',
              'евро': 'EUR'}


class ConvertionException(Exception):
    pass


class MoneyConvertion:

    @staticmethod
    def convertion(text_user):
        if len(text_user) != 3:
            print('Неверное количество параметров')
            return 'Неверное количество параметров'
            # raise ConvertionException('Неверное количество параметров')
        quote = text_user[0].lower()
        base = text_user[1].lower()

        if quote == base:
            print(f'Перевод двух одинаковых валют {quote} недопустим')
            return f'Перевод двух одинаковых валют {quote} недопустим'
            # raise ConvertionException(f'Перевод двух одинаковых валют {quote} недопустим')

        try:
            amount = float(text_user[2])
        except ValueError:
            print(f'неверно задано количество ({text_user[2]})')
            return f'неверно задано количество ({text_user[2]})'
            # raise ConvertionException(f'неверно задано количество ({text_user[2]})')

        try:
            quote_ticker = values_key[quote]
        except KeyError:
            print(f'Валюты {quote} нет в списке доступных')
            return f'Валюты {quote} нет в списке доступных'
            # raise ConvertionException(f'Валюты {quote} нет в списке доступных')

        try:
            base_ticker = values_key[base]
        except KeyError:
            print(f'Валюты {base} нет в списке доступных')
            return f'Валюты {base} нет в списке доступных'
            # raise ConvertionException(f'Валюты {base} нет в списке доступных')

        r = requests.get(f'https://api.exchangeratesapi.io/latest?base={quote_ticker}&symbols={base_ticker}')
        rate = json.loads(r.content)['rates'][base_ticker]
        text = f'Курс {amount} {quote_ticker} к {base_ticker} равен {rate * amount}'
        return text


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    text = 'Для конвертации валют введите команду в следующем формате:\n\
<имя валюты> <в какую валюту перевести> <количество вереводимой валюты>\n\
Увидеть список доступных валют /values'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def send_welcome(message):
    text = 'Доступные валюты'
    for key in values_key.keys():
        text = '\n'.join((text, key))

    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    text_user = message.text.split(' ')
    try:
        text = MoneyConvertion.convertion(text_user)
    except:
        bot.send_message(message.chat.id, 'Что-то пошло не так')
    else:
        bot.send_message(message.chat.id, text)


bot.polling()
