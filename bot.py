import telebot
from flask import Flask, request
import os
import time

bot_token = os.getenv('TOKEN')
port = int(os.environ.get('PORT', 5000))
bot = telebot.TeleBot(token=bot_token, parse_mode=None)
server = Flask(__name__)


def find_at(msg):
    # from a list of texts, it finds the one with the '@' sign
    for i in msg:
        if '@' in i:
            return i


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, 'Welcome!')


@bot.message_handler(commands=['help'])
def send_help(message):
    bot.reply_to(message, 'To use this bot, send it a username')


@bot.message_handler(func=lambda msg: msg.text is not None and '@' in msg.text)
# lambda function finds messages with the '@' sign in them
# in case msg.text doesn't exist, the handler doesn't process it
def at_converter(message):
    texts = message.text.split()
    at_text = find_at(texts)
    if at_text == '@':  # in case it's just the '@', skip
        pass
    else:
        insta_link = "https://instagram.com/{}".format(at_text[1:])
        bot.reply_to(message, insta_link)


@server.route('/' + bot_token, methods=['POST'])
def getMessage():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200


@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://enigmatic-mountain-38645.herokuapp.com/' +
                    bot_token)
    return "!", 200


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=port)
