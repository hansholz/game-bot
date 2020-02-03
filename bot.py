import telebot
import os, random
from telebot.types import Message
import linecache
import sqlite3


TOKEN = '1004071626:AAHHFv-_sYW7hu0qnrf827wuMFkHmtTv--k'


bot = telebot.TeleBot(TOKEN)
conn = sqlite3.connect('example.db')

answers = {}


@bot.message_handler(commands=['start'])
def send_welcome(message: Message):
    # sending a picture of country
    flag = random.choice(os.listdir("flags/"))
    answers[message.chat.id] = search_name_of_country(flag)
    photo = open('flags/'+flag, 'rb')
    photo = bot.send_photo(message.chat.id, photo, 'What country is this?')
    bot.register_next_step_handler(photo, checking)


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
    else:
        if message.text.strip().lower() == answers[message.chat.id].lower():
            bot.reply_to(message, f'You are damn right!  It is {answers[message.chat.id]} https://wikipedia.org/wiki/{answers[message.chat.id].replace(" ", "+")}')
        else:
            bot.reply_to(message, f'Try again!  It is {answers[message.chat.id]} https://wikipedia.org/wiki/{answers[message.chat.id].replace(" ", "_")}')
        return


bot.polling()
