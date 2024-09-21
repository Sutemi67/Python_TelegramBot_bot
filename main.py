import telebot
import webbrowser
from telebot import types
import requests
import json

bot = telebot.TeleBot("7557506732:AAHdCITiJTBAj-r_0M32oPNvZTNNLUk9v74")
weather_api = "985445d183837d778dc2a8e34937db9a"


@bot.message_handler(commands=['start'])
def main(message):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('Перейти на сайт', url='https://www.sbphoto.art/main')
    btn2 = types.InlineKeyboardButton('Удалить', callback_data='delete')
    btn3 = types.InlineKeyboardButton('Редактировать', callback_data='edit')
    markup.row(btn1)
    markup.row(btn2, btn3)

    markup = types.ReplyKeyboardMarkup()
    btn4 = types.KeyboardButton('Перейти на сайт')
    btn5 = types.KeyboardButton('Удалить')
    btn6 = types.KeyboardButton('Редактировать')
    markup.row(btn4)
    markup.row(btn5, btn6)
    bot.send_message(message.chat.id, f"Hello {message.from_user.first_name}", reply_markup=markup)


@bot.message_handler(content_types=['text'])
def get_weather(message):
    city = message.text.strip().lower()
    res = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_api}&units=metric")
    if res.status_code == 200:
        data = json.loads(res.text)
        temp = data['main']['temp']
        bot.reply_to(message, f"Температура сейчас: {temp}")
    else:
        bot.reply_to(message, "Такой город не найден")


@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    if callback.data == 'delete':
        bot.delete_message(callback.message.chat.id, callback.message.message_id - 1)
    elif callback.data == 'edit':
        bot.edit_message_text('Edit text', callback.message.chat.id, callback.message.message_id)


@bot.message_handler()
def info(message):
    if message.text.lower() == 'привет':
        bot.send_message(message.chat.id, 'че надо')


@bot.message_handler(commands=['site'])
def site(message):
    webbrowser.open('https://www.sbphoto.art/main')


@bot.message_handler(content_types=['photo', 'audio'])
def get_content(message):
    bot.reply_to(message, "Как здорово!")


bot.polling(none_stop=True)
