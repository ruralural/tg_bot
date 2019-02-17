from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import os
import feedparser
import yaml
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


updater = Updater(TELEGRAM_TOKEN)
dispatcher = updater.dispatcher
parser = feedparser.parse('https://www.reddit.com/r/aww/top.rss?t=week')


def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="I'm a bot, please talk to me!")

def echo(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text=update.message.text)

def forecast(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text=reddit_feed)
def feed(bot,update):
    reddit_feed = parser.entries[randint(0,10)]['link']
    bot.send_message(chat_id=update.message.chat_id, text=reddit_feed)
    
    
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

#echo_handler= MessageHandler(Filters.text, echo)
#dispatcher.add_handler(echo_handler)
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
