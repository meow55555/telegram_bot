import telebot
from flask import Flask, request
import os
import requests
from config import bot_token, user_token

bot = telebot.TeleBot(token=bot_token, parse_mode=None)
server = Flask(__name__)


def find_at(msg):
    # from a list of texts, it finds the one with the '@' sign
    for i in msg:
        if '@' in i:
            return i


@bot.message_handler(commands=['status'])
def send_welcome(message):
    headers = {"auth": user_token}
    r = requests.get('http://127.0.0.1:8080/api/status', headers=headers)
    bot.reply_to(message, r.content)


@bot.message_handler(commands=['status_verbose'])
def send_help(message):
    headers = {"auth": user_token}
    r = requests.get('http://127.0.0.1:8080/api/status?mode=verbose',
                     headers=headers)
    bot.reply_to(message, r.content)


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
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
