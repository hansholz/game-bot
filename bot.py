import telebot
from telebot.types import Message
from telebot import types
import sqlite3


with open("token.txt") as f:
    token = f.read().strip()
TOKEN = f'{token}'


bot = telebot.TeleBot(TOKEN)


answers = {}


initiators = {}


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
    answers[message.chat.id] = str(flag[0])
    try:
        with open(f'flags/{str(flag[1]).lower()}.png', 'rb') as image:
            bot.send_photo(message.chat.id, image, f'What country is this? ', reply_markup=key)
    except IOError:
        send_welcome(message)
    conn.close()


@bot.message_handler(commands=['help'])
def helping(message: Message):
    bot.send_message(message.chat.id, f'List of commands:\n'
                                      f'/start - start a new game\n'
                                      f'/battle - to cause anyone to fight')


@bot.message_handler(commands=['battle'])
def battle(message: Message):
    key = types.InlineKeyboardMarkup()
    loser = types.InlineKeyboardButton(text="I'm sheepish", callback_data="sheepish")
    agree = types.InlineKeyboardButton(text="Agree", callback_data="agree")
    key.add(loser)
    key.add(agree)
    bot.send_message(message.chat.id, f'Who wants to battle with {message.from_user.first_name}?', reply_markup=key)
    initiators[message.chat.id] = str(message.from_user.first_name)


@bot.message_handler(content_types=['text'])
def versus(message: Message, call):
    bot.send_message(message.chat.id, f'Lady and guys, tonight fight: {call.from_user.first_name} VS {initiators[message.chat.id]}')


@bot.message_handler(content_types=['text'])
def sheepish(message: Message, call):
    bot.send_message(message.chat.id, f'This hear everyone? {call.from_user.first_name} is sheepish)')


@bot.message_handler(content_types=['text'])
def checking(message: Message):
    # checking users answer
    key = types.InlineKeyboardMarkup()
    itembtn = types.InlineKeyboardButton(text="Next", callback_data="next")
    key.add(itembtn)
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
    elif call.data == "sheepish":
        sheepish(call.message, call)
    elif call.data == "agree":
        versus(call.message, call)
    return call


@bot.message_handler(content_types=['text'])
def give_up(message: Message):
    # answer, when user give up
    key = types.InlineKeyboardMarkup()
    itembtn = types.InlineKeyboardButton(text="Next", callback_data="next")
    key.add(itembtn)
    bot.send_message(message.chat.id, f'Pff... Really? It is {answers[message.chat.id]} https://wikipedia.org/wiki/{answers[message.chat.id].replace(" ", "_")}', reply_markup=key)


if __name__ == '__main__':
    bot.polling(none_stop=True)
