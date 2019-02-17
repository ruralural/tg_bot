from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import os
import feedparser
import yaml
import json
import urllib.request
from random import randint


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

def get_config(config_filename=None):
    if config_filename is None:
        config_filename = os.path.join(os.getcwd(), 'config.yaml')
    with open(config_filename) as config_file:
        return yaml.load(config_file.read())

config = get_config()
TELEGRAM_TOKEN = config['tokens']['telegram']
weather_api = config['tokens']['weather_api']


updater = Updater(TELEGRAM_TOKEN)
dispatcher = updater.dispatcher
parser = feedparser.parse('https://www.reddit.com/r/aww/top.rss?t=week')


def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Hi! try out !aww and !weather")

def echo(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text=update.message.text)

def forecast(bot, update):
    with urllib.request.urlopen(weather_api) as url:
        data = json.loads(url.read().decode())
        current_state = data['weather'][0]['main']
        current_temp = round(data['main']['temp'])
    bot.send_message(chat_id=update.message.chat_id, text="The sky "
                     "is {0} now and it's {1} degrees outside.".format(current_state.lower(),
                                                                       current_temp))
def feed(bot,update):
    reddit_feed = parser.entries[randint(0,10)]['link']
    bot.send_message(chat_id=update.message.chat_id, text=reddit_feed)
    
    
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

aww_handler = MessageHandler(Filters.regex(r'!aww'), feed)
dispatcher.add_handler(aww_handler)

forecast_handler = MessageHandler(Filters.regex(r'!weather'), forecast)
dispatcher.add_handler(forecast_handler)

updater.start_polling()

#if __name__ == "__main__":
#    filepath = "config.yaml"
#    data = yaml_loader(filepath)
#
#    updater = Updater(token=data['tokens']['bot'])
#    dispatcher = updater.dispatcher
