import telebot
import os, random
from telebot.types import Message
import linecache
from telebot import types
from telebot import logger
#import sqlite3


token = os.getenv("token")
TOKEN = f'{token}'


bot = telebot.TeleBot(TOKEN)
#conn = sqlite3.connect('example.db')

answers = {}


@bot.message_handler(commands=['start'])
def send_welcome(message: Message):
    # sending a picture of country
    key = types.InlineKeyboardMarkup()
    itembtn1 = types.InlineKeyboardButton(text="Next", callback_data="next")
    key.add(itembtn1)
    flag = random.choice(os.listdir("flags/"))
    answers[message.chat.id] = search_name_of_country(flag)
    photo = open('flags/'+flag, 'rb')
    photo = bot.send_photo(message.chat.id, photo, 'What country is this?', reply_markup=key)
    bot.register_next_step_handler(photo, checking)

    #bot.send_message(message.chat.id, f'{key}')


def del_trash(flag):
    # deleting a part of string with ".png"
    flagsiso = flag.replace(".png", "")
    return flagsiso


def line_num_for_phrase_in_file(flag, filename='list-of-iso.txt'):
    # returning a number of string with name of image this country
    flagsiso = del_trash(flag)
    with open(filename, 'r') as f:
        for (i, line) in enumerate(f):
            if str(flagsiso.upper()) in line:
                return i, line


def search_name_of_country(flag):
    # returning name of country by correlation numbers of strings
    i, line = line_num_for_phrase_in_file(flag)
    name_country = linecache.getline('list-of-countries.txt', (i+1))
    return name_country.strip()


@bot.message_handler(content_types=['text'])
def checking(message):
    if message.text == '/start':
        send_welcome(message)
    elif message.text == 'Next':
        send_welcome(message)
    else:
        if message.text.strip().lower() == answers[message.chat.id].lower():
            bot.reply_to(message, f'You are damn right! It is {answers[message.chat.id]} https://wikipedia.org/wiki/{answers[message.chat.id].replace(" ", "_")}')
        else:
            bot.reply_to(message, f'Try again! It is {answers[message.chat.id]} https://wikipedia.org/wiki/{answers[message.chat.id].replace(" ", "_")}')
        return


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.data == "next":
        send_welcome(call.message)
    return


if __name__ == '__main__':
    bot.polling(none_stop=True)
