import telebot
import os, random
from telebot.types import Message
import linecache
import sqlite3


TOKEN = '1004071626:AAHHFv-_sYW7hu0qnrf827wuMFkHmtTv--k'


bot = telebot.TeleBot(TOKEN)
conn = sqlite3.connect('example.db')


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message: Message):
        flag = random.choice(os.listdir("flags/"))
        photo = open('flags/'+flag, 'rb')
        bot.send_photo(message.chat.id, photo, 'What country is this??')
        return flag


@bot.message_handler()
def del_trash(flag):
        flagsiso = flag.replace(".png", "")
        return flagsiso


@bot.message_handler()
def line_num_for_phrase_in_file(flagsiso, filename='list-of-iso.txt'):
    with open(filename, 'r') as f:
        for (i, line) in enumerate(f):
            if str(flagsiso.upper()) in line:
                return i, line


@bot.message_handler()
def search_name_of_country(i):
    name_country = linecache.getline('list-of-countries.txt', (i+1))
    return name_country


@bot.message_handler()
def checking(message, name_country):
    if message.text == name_country:
        print(name_country)
        bot.reply_to(message, 'You are damn right!')
    else:
        bot.reply_to(message, 'Try again!')
        return


bot.polling()
