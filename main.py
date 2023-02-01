import telebot
from config import TOKEN, values_dict
from extensions import APIException, Converter

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    mess = f'Привет, {message.from_user.first_name}! Я конвертирую валюту!\nНапиши /help, ' \
           f'чтобы узнать информацию о боте.\nНапиши /values, чтобы узнать какую валюту я могу перевести.\n'
    bot.send_message(message.chat.id, mess)


@bot.message_handler(commands=['help'])
def help(message):
    mess = f'Чтобы узнать, как перевести одну валюту в другую, введите сообщение в формате:\n' \
           f'<имя валюты> <в какую валюту перевести> <количество валюты>. Например: Евро Рубль 100'
    bot.send_message(message.chat.id, mess)


@bot.message_handler(commands=['values'])
def values(message):
    mess = f'Доступные валюты: Евро, Доллар, Рубль.'
    bot.send_message(message.chat.id, mess)


@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    message_text = message.text.title().split(' ')
    try:
        if len(message_text) != 3:
            raise APIException('Введите три параметра.')
        quote, base, amount = message_text
        result = Converter.get_price(quote, base, amount)
    except APIException as apie:
        bot.reply_to(message, f'Ошибка пользователя.\n{apie}')
    else:
        text = f'{amount}  {values_dict[quote]} = {result}  {values_dict[base]}'
        bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)
