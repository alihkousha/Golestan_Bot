from telegram import KeyboardButton, ReplyKeyboardMarkup, Update
from telegram.ext import (Updater, CommandHandler, ConversationHandler, MessageHandler, Filters, CallbackContext)
from Golestan_Crawler import Golestan_Crawler as GC
import os

TOKEN = os.environ.get("TOKEN")
class Golestan_Bot:

    def __init__(self) -> None:
        self.keyboard = [[KeyboardButton('Add remainder'), KeyboardButton('Add dude'), KeyboardButton('Add No')],
                         [KeyboardButton('Add re'), KeyboardButton('Add dud'), KeyboardButton('Add N')],
                         [KeyboardButton('Add rem'), KeyboardButton('Add du'), KeyboardButton('Add')]]


    def start_handler(self, update, context):
        update.message.reply_text('dhf')
        crawler = GC("chromedriver.exe")
        crawler.Threading_Crawler(update,context)

if __name__ == "__main__":
    Bot = Golestan_Bot()
    updater = Updater(TOKEN)
    updater.dispatcher.add_handler(CommandHandler("start", Bot.start_handler))
    updater.start_polling()