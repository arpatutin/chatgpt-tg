import telebot
from telebot.types import *

from config import TELEGRAM_KEY
from db import *
from datetime import datetime

bot = telebot.TeleBot(TELEGRAM_KEY)
locales = read_locales()
sessions = read_sessions()
actives = read_actives()


@bot.callback_query_handler(func=lambda _: True)
def set_locale(call: CallbackQuery):
    global locales, sessions, actives
    if call.data in ["set_ru_locale", "set_en_locale"]:
        if call.data == "set_ru_locale":
            locales[call.from_user.id] = ru_locale
            write_to_locales(call.from_user.id, "ru")
        elif call.data == "set_en_locale":
            locales[call.from_user.id] = en_locale
            write_to_locales(call.from_user.id, "en")
        bot.answer_callback_query(call.id, locales[call.from_user.id]["SUCCESS"])
        sessions[call.from_user.id] = {}
        actives[call.from_user.id] = [False]
        write_to_actives(call.from_user.id, [False])
        bot.send_message(call.message.chat.id, locales[call.from_user.id]["HELLO"])
        bot.send_message(call.message.chat.id, locales[call.from_user.id]["HELP"])
    else:
        actives[call.from_user.id] = [True, sessions[call.from_user.id][call.data.replace('-', ' ')]]
        bot.answer_callback_query(call.id, locales[call.from_user.id]["SUCCESS"])
        bot.send_message(call.message.chat.id, locales[call.from_user.id]["SESSIONS_LIST_SUCCESS"])


@bot.message_handler(commands=["start", "changelang"])
def start(message: Message):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("English🇺🇸", callback_data="set_en_locale"))
    markup.add(InlineKeyboardButton("Русский🇷🇺", callback_data="set_ru_locale"))
    bot.send_message(message.chat.id, "Choose your language / Выберите свой язык", reply_markup=markup)


@bot.message_handler(commands=["help"])
def help_(message: Message):
    bot.send_message(message.chat.id, locales[message.from_user.id]["HELP"])


@bot.message_handler(commands=["startconversation"])
def startconversation(message: Message):
    global sessions, actives
    if False in actives[message.from_user.id]:
        lang = 'ru'
        if locales[message.from_user.id] == en_locale:
            lang = 'en'
        session = Session(lang=lang)
        session.title = datetime.now().strftime(locales[message.from_user.id]["SESSION_BASE_TITLE"])
        actives[message.from_user.id] = [True, session]
        write_to_actives(message.from_user.id, [True, session])
        bot.send_message(message.chat.id, locales[message.from_user.id]["SESSION_OPEN"])
    else:
        bot.send_message(message.chat.id, locales[message.from_user.id]["SESSION_ALREADY_OPEN"])


@bot.message_handler(commands=["quitconversation"])
def quitconversation(message: Message):
    global actives
    if True in actives[message.from_user.id]:
        actives[message.from_user.id] = [False]
        write_to_actives(message.from_user.id, [False])
        bot.send_message(message.chat.id, locales[message.from_user.id]["SESSION_QUIT"])
    else:
        bot.send_message(message.chat.id, locales[message.from_user.id]["SESSION_NOTHING_QUIT"])


@bot.message_handler(commands=["rejoinconversation"])
def rejoinconversation(message: Message):
    if False in actives[message.from_user.id]:
        markup = InlineKeyboardMarkup()
        for conv in sessions[message.from_user.id].keys():
            markup.add(InlineKeyboardButton(conv, callback_data=conv.replace(' ', '-')))
        bot.send_message(message.chat.id, locales[message.from_user.id]["SESSIONS_LIST"], reply_markup=markup)
    else:
        bot.send_message(message.chat.id, locales[message.from_user.id]["SESSIONS_LIST_CANT"])


@bot.message_handler(content_types=['text'])
def textmessage(message: Message):
    if True in actives[message.from_user.id]:
        msg = bot.send_message(message.chat.id, locales[message.from_user.id]["PLEASE_WAIT"], parse_mode='Markdown')
        session = actives[message.from_user.id][1]
        answer = session.new_message(message.text)
        if answer == -1:
            answer = locales[message.from_user.id]["ERROR"]
        if message.from_user.id not in sessions:
            sessions[message.from_user.id] = {}
        sessions[message.from_user.id][session.title] = session
        write_to_sessions(message.from_user.id, session)
        bot.delete_message(message.chat.id, msg.id)
        bot.send_message(message.chat.id, answer)
    else:
        msg = bot.send_message(message.chat.id, locales[message.from_user.id]["PLEASE_WAIT"], parse_mode='Markdown')
        answer = Session.ask_ai(message.text)
        if answer == -1:
            answer = locales[message.from_user.id]["ERROR"]
        bot.delete_message(message.chat.id, msg.id)
        bot.send_message(message.chat.id, answer)


bot.polling(non_stop=True)
