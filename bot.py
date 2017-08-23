from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import telegram
import urllib2
import logging
import dill
import os
from threading import Timer
import keys

def start(bot, update):
    update.message.reply_text(
        'Hi {}'.format(update.message.from_user.first_name))
    schedule_keyboard = [['Once a day', 'Twice a day'],
                         ['Once a week']]
    reply_markup = telegram.ReplyKeyboardMarkup(schedule_keyboard, 
                                                one_time_keyboard=True)
    print "hi %s" % reply_markup
    bot.send_message(chat_id=update.message.chat.id, 
                     text="Choose a cat delivery frequency", 
                     reply_markup=reply_markup)

def stop(bot, update):
    if os.path.exists('chats.p'):
        with open('chats.p') as o_chat:
            chats = dill.load(o_chat)
    chats[update.message.chat_id].cancel()

def send_cat(bot, update):
    c_id = update.message.chat_id
    bot.send_chat_action(chat_id=c_id, action=telegram.ChatAction.TYPING)
    bot.send_photo(chat_id=c_id, photo=urllib2.urlopen(keys.cat_url).geturl())

def parse_message_response(bot, update):
    chat_id = update.message.chat_id
    user_response = update.message.text.lower()
    
    if os.path.exists('chats.p'):
        with open('chats.p') as o_chat:
            chats = dill.load(o_chat)
    else:
        chats = {}
        with open('chats.p', 'w') as o_chat:
            dill.dump(chats, o_chat)

    if user_response == "once a day":
        send_cat(bot, update)
        timer = Timer(10, send_cat, [bot, update])
        timer.start()
        chats[chat_id] = timer
    elif user_response == "twice a day":
        send_cat(bot, update)
        timer = Timer(10, send_cat, [bot, update])
        timer.start()
        chats[chat_id] = timer
    elif user_response == "once a week":
        send_cat(bot, update)
        timer = Timer(10, send_cat, [bot, update])
        timer.start()
        chats[chat_id] = timer
    elif user_response == "test":
        send_cat(bot, update)
        timer = Timer(10, send_cat, [bot, update])
        timer.start()
        chats[chat_id] = timer
    elif user_response == "stop":
        bot.send_message(chat_id=chat_id, text="Bye")
        chats[chat_id].cancel()

    with open('chats.p', 'w') as o_chat:
        dill.dump(chats, o_chat)

print keys.bot_key
updater = Updater(keys.bot_key)
dispatcher = updater.dispatcher

dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('cat', send_cat))
dispatcher.add_handler(CommandHandler('stop', stop))
dispatcher.add_handler(MessageHandler(Filters.text, parse_message_response))

updater.start_polling()
updater.idle()