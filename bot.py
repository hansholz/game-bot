import telebot
import os, random
from telebot.types import Message
import linecache
import sqlite3


TOKEN = '1004071626:AAHHFv-_sYW7hu0qnrf827wuMFkHmtTv--k'


bot = telebot.TeleBot(TOKEN)
conn = sqlite3.connect('example.db')


@bot.message_handler(commands=['start', 'help'])
class Main:
    def send_welcome(self, message: Message):
        # sending a picture of country
        flag = random.choice(os.listdir("flags/"))
        photo = open('flags/'+flag, 'rb')
        bot.send_photo(message.chat.id, photo, 'What country is this??')
        return flag

    def del_trash(self, flag):
        # deleting a part of string with ".png"
        flagsiso = flag.replace(".png", "")
        return flagsiso

    def line_num_for_phrase_in_file(self, flagsiso, filename='list-of-iso.txt'):
        # returning a number of string with name of image this country
        with open(filename, 'r') as f:
            for (i, line) in enumerate(f):
                if str(flagsiso.upper()) in line:
                    return i, line

    def search_name_of_country(self, i):
        # returning name of country by correlation numbers of strings
        name_country = linecache.getline('list-of-countries.txt', (i+1))
        return name_country


    def checking(self, message, name_country):
        # checking answer of user with correct name of country
        if message.text == name_country:
            print(name_country)
            bot.reply_to(message, 'You are damn right!')
        else:
            bot.reply_to(message, 'Try again!')
            return


bot.polling()
