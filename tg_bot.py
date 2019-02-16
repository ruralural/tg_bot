from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import feedparser
from random import randint

updater = Updater(token=TOKEN)
dispatcher = updater.dispatcher
parser = feedparser.parse('https://www.reddit.com/r/aww/top.rss?t=week')

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
#reddit_feed = parser.entries[randint(0,10)]['link']

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
forecast_handler = MessageHandler(Filters.regex(r'!cute'), feed)
dispatcher.add_handler(forecast_handler)

updater.start_polling()
