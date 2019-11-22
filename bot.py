import telebot
import os, random
from telebot.types import Message
import linecache

TOKEN = '1004071626:AAHHFv-_sYW7hu0qnrf827wuMFkHmtTv--k'

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(content_types=['photo', 'text'])
def send_flag(message: Message):
    if 'next' in message.text:
        flag = random.choice(os.listdir("flags/"))
        photo = open('flags/'+flag, 'rb')
        bot.send_photo(message.chat.id, photo, 'What is country?')
        return flag


@bot.message_handler(content_types=['text'])
def send_message(message: Message, flag):
    if 'opt' in message.text:
        bot.send_message(message.chat.id, str(flag))
        flagvar = flag
        flagsiso = flagvar.replace(".png", "")
        return flagsiso


def del_trash(flag, message):
    if '1' in message.text:
        bot.send_message(message.chat.id, str(flag))
        flagvar = str(flag)
        flagsiso = flagvar.replace(".png", "")
    return


def line_num_for_phrase_in_file(flagiso, filename='list-of-iso.txt'):
    with open(filename,'r') as f:
        for (i, line) in enumerate(f):
            if str(flagiso) in line:
                return i, line


def search_name_of_country(i):
    name_country = linecache.getline('list-of-countries.txt', i)
    return name_country


bot.polling()
