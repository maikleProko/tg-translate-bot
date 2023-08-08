from flask import Flask
from threading import Thread
from googletrans import Translator

app = Flask('')
translator = Translator()


@app.route('/')
def home():
    return "I'm alive"


def run():
    app.run(host='0.0.0.0', port=80)


def keep_alive():
    t = Thread(target=run)
    t.start()


def execute(bot, message, src, dest):
    bot.send_message(message.from_user.id,
                     translator.translate(message.text, src=src, dest=dest).text
    )


def is_valid_lang(lang):
    try:
        translator.translate('abc', src='en', dest=lang).text
    except ValueError as e:
        if str(e) != 'invalid destination language':
            raise
        else:
            return False
    return True
