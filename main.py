import telebot
import webbrowser
from telebot import types
import requests
import json
from currency_converter import CurrencyConverter

bot = telebot.TeleBot("7557506732:AAHdCITiJTBAj-r_0M32oPNvZTNNLUk9v74")
weather_api = "985445d183837d778dc2a8e34937db9a"
currency = CurrencyConverter()
chatID = 0


@bot.message_handler(commands=['start'])
def main(message):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('Перейти на сайт', url='https://www.sbphoto.art/main')
    btn2 = types.InlineKeyboardButton('Узнать погоду', callback_data='weather')
    btn3 = types.InlineKeyboardButton('Курс валюты', callback_data='currency')
    markup.add(btn1, btn2, btn3)

    bot.send_message(message.chat.id, f"Привет, {message.from_user.first_name}", reply_markup=markup)
    global chatID
    chatID = message.chat.id


@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    if callback.data == 'weather':
        bot.send_message(chatID, 'Чтобы узнать погоду напиши вопрос в любом из форматов\n"погода Смоленск"\n"Погода москва"')
    elif callback.data == 'currency':
        bot.send_message(chatID, 'погоду пока поспрашивай')


@bot.message_handler(content_types=['text'])
def get_weather(message):
    last_word = message.text.split()[-1]
    last_word_lower = last_word.lower()
    if message.text == f"погода {last_word}":
        res = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={last_word_lower}&appid={weather_api}&units=metric")
        if res.status_code == 200:
            data = json.loads(res.text)
            temp = data['main']['temp']
            humidity = data['main']['humidity']
            wind = data['wind']["speed"]
            bot.reply_to(message, f"Температура сейчас: {temp}\nВлажность: {humidity}\nВетер: {wind}м/с")
        else:
            bot.reply_to(message, "Такой город не найден")
    elif message.text == f"Погода {last_word}":
        res = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={last_word_lower}&appid={weather_api}&units=metric")
        if res.status_code == 200:
            data = json.loads(res.text)
            temp = data['main']['temp']
            humidity = data['main']['humidity']
            wind = data['wind']["speed"]
            bot.reply_to(message, f"Температура сейчас: {temp}\nВлажность: {humidity}\nВетер: {wind}м/с")
        else:
            bot.reply_to(message, "Такой город не найден")


@bot.message_handler(commands=['site'])
def site():
    webbrowser.open('https://www.sbphoto.art/main')


@bot.message_handler(content_types=['photo', 'audio', 'video'])
def get_content(message):
    bot.reply_to(message, "Как здорово! Молодец, кидай еще))")


# bot.edit_message_text('Edit text', callback.message.chat.id, callback.message.message_id)
# bot.delete_message(callback.message.chat.id, callback.message.message_id - 1)

bot.polling(none_stop=True)
