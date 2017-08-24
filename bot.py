from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, InlineQueryHandler, Job
import telegram
from telegram import InlineQueryResultArticle, ParseMode, \
    InputTextMessageContent
import urllib2
import os
import keys

def start(bot, update):
    update.message.reply_text(
        'Hi {}'.format(update.message.from_user.first_name))
    schedule_keyboard = [['Once a day', 'Twice a day'],
                         ['Once a week']]
    reply_markup = telegram.ReplyKeyboardMarkup(schedule_keyboard, 
                                                one_time_keyboard=True)
    print "hi %s" % reply_markup
    bot.send_message(chat_id=update.message.chat_id, 
                     text="Choose a cat delivery frequency", 
                     reply_markup=reply_markup)

def stop(bot, update):
    jobs[update.message.chat_id].schedule_removal()
    bot.send_message(chat_id=update.message.chat_id, 
                     text="Cat delivered stopped")

def cat(bot, update):
    send_cat(bot, update.message.chat_id)

def send_cat(bot, c_id):
    bot.send_chat_action(chat_id=c_id,
                         action=telegram.ChatAction.TYPING)
    bot.send_photo(chat_id=c_id,
                   photo=urllib2.urlopen(keys.cat_url).geturl())

def inlinequery(bot, update):
    send_cat(bot, update.message.chat_id)

def cat_callback(bot, job):
    send_cat(bot, job.context)

def parse_message_response(bot, update, job_queue):
    chat_id = update.message.chat_id
    user_response = update.message.text.lower()

    if user_response == "fast":
        job = Job(cat_callback, 10.0, context=chat_id)
        jobs[chat_id] = job
        jq.put(job, next_t=0.0)
    elif user_response == "once a day":
        job = Job(cat_callback, 60*60*24, context=chat_id)
        jobs[chat_id] = job
        jq.put(job, next_t=0.0)
    elif user_response == "twice a day":
        job = Job(cat_callback, 60*30*24, context=chat_id)
        jobs[chat_id] = job
        jq.put(job, next_t=0.0)
    elif user_response == "once a week":
        job = Job(cat_callback, 60*60*24*7, context=chat_id)
        jobs[chat_id] = job
        jq.put(job, next_t=0.0)
    elif user_response == "stop":
        stop(bot, update)

updater = Updater(keys.bot_key)

jobs = {}
jq = updater.job_queue
dp = updater.dispatcher

dp.add_handler(CommandHandler('start', start))
dp.add_handler(CommandHandler('stop', stop))
dp.add_handler(CommandHandler('cat', cat))
dp.add_handler(InlineQueryHandler(inlinequery))

# dp.add_handler(MessageHandler(Filters.text, parse_message_response, pass_job_queue=True))

updater.start_polling()
updater.idle()