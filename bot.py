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


opponents = {}


initiators_coins = {}
initiators_coins[0] = 0


opponents_coins = {}
opponents_coins[0] = 0


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
    return


@bot.message_handler(commands=['help'])
def helping(message: Message):
    bot.send_message(message.chat.id, f'List of commands:\n'
                                      f'/start - start a new game\n'
                                      f'/battle - to cause anyone to fight')
    return


@bot.message_handler(commands=['battle'])
def battle(message: Message):
    key = types.InlineKeyboardMarkup()
    loser = types.InlineKeyboardButton(text="I'm sheepish", callback_data="sheepish")
    agree = types.InlineKeyboardButton(text="Agree", callback_data="agree")
    key.add(loser)
    key.add(agree)
    bot.send_message(message.chat.id, f'Who wants to battle with {message.from_user.first_name}?', reply_markup=key)
    initiators[message.chat.id] = message.from_user.first_name
    return


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    # checking which button have been pressed
    if call.data == "next":
        send_welcome(call.message)
    elif call.data == "give_up":
        give_up(call.message)
    elif call.data == "sheepish":
        sheepish(call.message)
    elif call.data == "agree":
        opponents[call.message.chat.id] = call.from_user.first_name
        versus(call.message)
    return


@bot.message_handler(content_types=['text'])
def checking(message: Message):
    # checking users answer
    key = types.InlineKeyboardMarkup()
    itembtn = types.InlineKeyboardButton(text="Next", callback_data="next")
    key.add(itembtn)
    if message.text.strip().lower() == answers[message.chat.id].lower():
        bot.reply_to(message, f'You are damn right! It is {answers[message.chat.id]} https://wikipedia.org/wiki/'
                              f'{answers[message.chat.id].replace(" ", "_")}', reply_markup=key)
    else:
        bot.reply_to(message, f'Try again! It is {answers[message.chat.id]} https://wikipedia.org/wiki/'
                              f'{answers[message.chat.id].replace(" ", "_")}', reply_markup=key)
    try:
        checking_initiator(message)
        checking_opponents(message)
    except KeyError:
        return


@bot.message_handler(content_types=['text'])
def give_up(message: Message):
    # answer, when user give up
    key = types.InlineKeyboardMarkup()
    itembtn = types.InlineKeyboardButton(text="Next", callback_data="next")
    key.add(itembtn)
    bot.send_message(message.chat.id, f'Pff... Really? It is {answers[message.chat.id]} https://wikipedia.org/wiki/'
                                      f'{answers[message.chat.id].replace(" ", "_")}', reply_markup=key)
    return


@bot.message_handler(content_types=['text'])
def sheepish(message: Message):
    bot.send_message(message.chat.id, f'This hear everyone? {opponents[message.chat.id]} is sheepish)')
    return


@bot.message_handler(content_types=['text'])
def versus(message: Message):
    if opponents[message.chat.id] == initiators[message.chat.id]:
        bot.send_message(message.chat.id, f'{initiators[message.chat.id]} wants to fight the shadow')
    else:
        bot.send_message(message.chat.id, f'Lady and guys, tonight fight: {opponents[message.chat.id]} VS'
                                      f' {initiators[message.chat.id]}')
        bot.send_message(message.chat.id, f'Initiator of battle {initiators[message.chat.id]} is first')
        send_welcome(message)
    return


@bot.message_handler(content_types=['text'])
def checking_initiator(message: Message):
    if message.from_user.first_name == initiators[message.chat.id]:
        if answers[message.chat.id].lower() == message.text.strip().lower():
            i = initiators_coins[0]
            i += 1
            if i == 10:
                bot.send_message(message.chat.id, f'{initiators[message.chat.id]} won this battle!!! He have {i} points')
                initiators_coins[0] = 0
                opponents_coins[0] = 0
                initiators[message.chat.id] = ''
                opponents[message.chat.id] = ''
            else:
                bot.send_message(message.chat.id, f'{initiators[message.chat.id]} have {i} points')
                initiators_coins[0] = i
    else:
        return


@bot.message_handler(content_types=['text'])
def checking_opponents(message: Message):
    if message.from_user.first_name == opponents[message.chat.id]:
        if answers[message.chat.id].lower() == message.text.strip().lower():
            k = opponents_coins[0]
            k += 1
            if k == 10:
                bot.send_message(message.chat.id, f'{opponents[message.chat.id]} won this battle!!! He have {k} points')
                opponents_coins[0] = 0
                initiators_coins[0] = 0
                initiators[message.chat.id] = ''
                opponents[message.chat.id] = ''
            else:
                bot.send_message(message.chat.id, f'{opponents[message.chat.id]} have {k} points')
                opponents_coins[0] = k
        else:
            return


bot.skip_pending = True
bot.polling(none_stop=True, interval=0)
