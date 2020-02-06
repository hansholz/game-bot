import telebot
import threading
from telebot.types import Message
import linecache
from telebot import types
import sqlite3


with open("token.txt") as f:
    token = f.read().strip()
TOKEN = f'{token}'


bot = telebot.TeleBot(TOKEN)


answers = {}


@bot.message_handler(commands=['start'])
def send_welcome(message: Message):
    # sending a picture of country
    key = types.InlineKeyboardMarkup()
    itembtn = types.InlineKeyboardButton(text="I give up", callback_data="give_up")
    key.add(itembtn)

    conn = sqlite3.connect('data1.sqlite')
    c = conn.cursor()
    c.execute('SELECT * FROM countries ORDER BY RANDOM() LIMIT 1;')
    conn.commit()

    data = list(c)
    flag = [item for t in data for item in t]
    varu = str(flag[1])
    answers[message.chat.id] = search_name_of_country(varu)
    photo = open(f'flags/{varu.lower()}.png', 'rb')
    bot.send_photo(message.chat.id, photo, 'What country is this?', reply_markup=key)

    conn.close()


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
def checking(message: Message):
    key = types.InlineKeyboardMarkup()
    itembtn = types.InlineKeyboardButton(text="Next", callback_data="next")
    key.add(itembtn)
    if answers.get(message.chat.id):
        if message.text.strip().lower() == answers[message.chat.id].lower():
            bot.reply_to(message, f'You are damn right! It is {answers[message.chat.id]} https://wikipedia.org/wiki/{answers[message.chat.id].replace(" ", "_")}', reply_markup=key)
        else:
            bot.reply_to(message, f'Try again! It is {answers[message.chat.id]} https://wikipedia.org/wiki/{answers[message.chat.id].replace(" ", "_")}', reply_markup=key)
        return


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    # checking which button have been pressed
    if call.data == "next":
        send_welcome(call.message)
    elif call.data == "give_up":
        give_up(call.message)
    return


@bot.message_handler(content_types=['text'])
def give_up(message: Message):
    # answer, when user give up
    key = types.InlineKeyboardMarkup()
    itembtn = types.InlineKeyboardButton(text="Next", callback_data="next")
    key.add(itembtn)
    bot.send_message(message.chat.id, f'Pff... Really? It is {answers[message.chat.id]} https://wikipedia.org/wiki/{answers[message.chat.id].replace(" ", "_")}', reply_markup=key)


if __name__ == '__main__':
    bot.polling(none_stop=True)
