from telebot.types import *
import telebot


from config import *
from locales.ru import *
from locales.en import *

bot = telebot.TeleBot(TELEGRAM_KEY)
locales = {}  # User ID: locale
sessions = {}


# db


@bot.callback_query_handler(func=lambda _: True)
def set_locale(call: CallbackQuery):
    global locales
    if call.data in ["set_ru_locale", "set_en_locale"]:
        if call.data == "set_ru_locale":
            locales[call.from_user.id] = ru_locale
        elif call.data == "set_en_locale":
            locales[call.from_user.id] = en_locale
        bot.answer_callback_query(call.id, "OK")
        bot.send_message(call.message.chat.id, locales[call.from_user.id]["HELLO"])
        bot.send_message(call.message.chat.id, locales[call.from_user.id]["HELP"])


@bot.message_handler(commands=["start"])
def start(message: Message):
    if locales.get(message.from_user.id) is None:
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("Русский", callback_data="set_ru_locale"))
        markup.add(InlineKeyboardButton("English", callback_data="set_en_locale"))
        bot.send_message(message.chat.id, "Choose your language / Выберите свой язык", reply_markup=markup)


@bot.message_handler(commands=["help"])
def help_(message: Message):
    bot.send_message(message.chat.id, locales[message.from_user.id]["HELP"])


@bot.message_handler(commands=["startconversation"])
def startconversation(message: Message):
    pass


@bot.message_handler(commands=["quitconversation"])
def quitconversation(message: Message):
    pass


@bot.message_handler(commands=["rejoinconversation"])
def rejoinconversation(message: Message):
    pass


@bot.message_handler(commands=["finishconversation"])
def finishconversation(message):
    pass


bot.polling(non_stop=True)
