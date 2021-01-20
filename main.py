import telebot
from utils import MoneyConvertion
from config import TOKEN, values_key

bot = telebot.TeleBot(TOKEN)

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
