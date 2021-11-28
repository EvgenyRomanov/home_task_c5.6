import telebot
from config import keys, TOKEN
from extensions import Converter, APIException


bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Для начала работы введите команду в формате:\n<имя валюты, цену которой хотите узнать> \
<имя валюты, в которой надо узнать цену первой валюты> <количество первой валюты>\
\nУвидеть список доступных валют: /values' 
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = text + f'\n- {key}'
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        param = message.text.split(' ')
        
        if len(param) != 3:
            raise APIException('Неверное количесто параметров.')
        else:
            quote, base, amount = param
            total_base = Converter.get_price(base, quote, amount)
            
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду.\n{e}')
    else:    
        text = f'Цена {amount} {quote} в {base} - {total_base}.'
        bot.send_message(message.chat.id, text)


bot.polling()

