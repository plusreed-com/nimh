import logging
from telegram.ext import Updater, MessageHandler, CommandHandler, Filters

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

btoken = "" # Put your bot token here.
banned_ids = [  # These people cannot talk, all their messages are filtered and censored.
    # Add IDs here
	# Example:
	# 123456,
	# 123457,
	# 123555,
]
banned_text_msg = [  # These messages are deleted instantly if they match a string within this list.
    # Add messages here
	# Example
	# "this message is bad and will get deleted!",
	# "this message is also bad!",
]
owner_ids = [
    # Put your Telegram ID here. This can house multiple people.
	# Example:
	# 775485438,
	# 847598437,
]
log_chan = '@PUBLIC_CHANNEL_NAME_HERE' # this is where nimh will log its actions.


def delmsg(bot, update):
    mid = update.message.from_user
    mtxt = update.message.text
    if mid.id in banned_ids:
        print("MESSAGE DELETED - More info in {0}".format(log_chan))
        update.message.delete()
        bot.send_message(chat_id=log_chan, text="Censored message from Telegram.User: {0} with text '{1}'.".format(str(mid), mtxt))
    elif mtxt in banned_text_msg:
        print("MESSAGE DELETED - More info in {0}".format(log_chan))
        update.message.delete()
        bot.send_message(chat_id=log_chan,
                         text="Censored message from Telegram.User: {0} with text '{1}'. Text matched string in list.".format(str(mid), mtxt))


def pingcmd(bot, update):
    mid = update.message.from_user
    if mid.id in owner_ids:
        print("PING COMMAND - More info in {0}".format(log_chan))
        update.message.reply_text('pong! hello, {0}!'.format(update.message.from_user.first_name))
        bot.send_message(chat_id=log_chan, text="Ping command from {0}".format(update.message.from_user.first_name))


def listids(bot, update):
    mid = update.message.from_user
    print("LISTIDS command")
    if mid.id in owner_ids:
        update.message.reply_text(str(banned_ids))


updater = Updater(token=btoken)
d = updater.dispatcher


d.add_handler(CommandHandler('ping', pingcmd))
d.add_handler(CommandHandler('listids', listids))
d.add_handler(MessageHandler(Filters.all, delmsg))


updater.start_polling()
print("bot is ready, press ^C twice to break!")
print("--- logs ---")
updater.idle()
