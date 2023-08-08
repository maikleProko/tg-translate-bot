from telebot import types
import constants
from routes.routes import keep_alive, execute, is_valid_lang
from utils.switch import switch
import pip

pip.main(['install', 'pytelegrambotapi'])
import telebot

bot = telebot.TeleBot(constants.TOKEN)

options = {
    'src': 'ru',
    'dest': 'en',
    'mode': 'default'
}


def change_mode(mode, message, answer):
    options['mode'] = mode
    bot.send_message(message.from_user.id, answer)


def change_lang(option, message):
    if is_valid_lang(message.text):
        options['mode'] = 'default'
        options[option] = message.text
        bot.send_message(message.from_user.id, constants.OPTIONS_AGREE)
    else:
        bot.send_message(message.from_user.id, constants.OPTIONS_DISAGREE)


def send_start_message(message):
    markup = types.ReplyKeyboardMarkup()
    src_button = types.KeyboardButton(constants.OPTIONS_SRC_MENU)
    dest_button = types.KeyboardButton(constants.OPTIONS_DEST_MENU)
    markup.add(src_button, dest_button)
    bot.send_message(message.from_user.id, constants.START_MESSAGE, reply_markup=markup)


def process_message(message, current_mode):
    for case in switch(message.text, current_mode):
        if case('/start', 'default'):
            send_start_message(message)
            break
        if case(constants.OPTIONS_SRC_MENU, 'default'):
            change_mode('src', message, constants.OPTIONS_SRC_MESSAGE)
            break
        if case(constants.OPTIONS_DEST_MENU, 'default'):
            change_mode('dest', message, constants.OPTIONS_DEST_MESSAGE)
            break
        if case('src'):
            change_lang('src', message)
            break
        if case('dest'):
            change_lang('dest', message)
            break
        if case('default'):
            execute(bot, message, options['src'], options['dest'])
            break
        if case():
            break


@bot.message_handler(content_types=['text'])
def get_text_message(message):
    process_message(message, options['mode'])


keep_alive()
bot.polling(non_stop=True, interval=0)
