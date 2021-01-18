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
    quote, base, amount = message.text.split(' ')
    r = requests.get(f'https://api.exchangeratesapi.io/latest?base={values_key[quote]}&symbols={values_key[base]}')
    rate = json.loads(r.content)['rates'][values_key[base]]
    text = f'Курс {amount} {values_key[quote]} к {values_key[base]} равен {rate * float(amount)}'
    bot.send_message(message.chat.id, text)


bot.polling()
