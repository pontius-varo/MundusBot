# MundusBot script #
from lib import utilities
from lib import mundusfuncs
# Always import custom just in case, even if file is empty
from lib import custom
from telegram.ext import CommandHandler, Updater, MessageHandler, Filters
version = 2.0  # BLOOD

# == Global Variables ==#

# Connection to Database
db = utilities.returnSetting('server_database')
db_connection = utilities.create_connection(db)

# Telegram Chat Token #
token = utilities.returnSetting('bot_token')
# Updater Object #
updater = Updater(token, use_context=True)
# Dispatcher #
dispatcher = updater.dispatcher

# ===== Commands =====#


def getUser(update, context):
    if context.args == []:
        username = utilities.formatUserName(update)

    else:
        username = context.args[0]

    telegram_msg = utilities.catchDebug(
        mundusfuncs.getUserInfo(username, db_connection))

    context.bot.send_message(
        chat_id=update.effective_chat.id, text=(telegram_msg))


def addUser(update, context):
    username = utilities.formatUserName(update)

    telegram_msg = utilities.catchDebug(
        mundusfuncs.addUsertoDb(username, db_connection))

    context.bot.send_message(
        chat_id=update.effective_chat.id, text=(telegram_msg)
    )


def addInfo(update, context):
    username = utilities.formatUserName(update)

    telegram_msg = utilities.catchDebug(
        mundusfuncs.addData(username, context.args, db_connection))

    context.bot.send_message(
        chat_id=update.effective_chat.id, text=(telegram_msg)
    )


def updateStatus(update, context):

    username = utilities.formatUserName(update)

    telegram_msg = utilities.catchDebug(mundusfuncs.updateUserStatus(
        username, context.args, db_connection))

    context.bot.send_message(
        chat_id=update.effective_chat.id, text=(telegram_msg)
    )


def getStatus(update, context):

    if context.args == []:
        username = utilities.formatUserName(update)
    else:
        username = context.args[0]

    telegram_msg = utilities.catchDebug(
        mundusfuncs.getUserStatus(username, db_connection))

    context.bot.send_message(
            chat_id=update.effective_chat.id, text=(telegram_msg)
        )

# Help


def getHelp(update, context):
    telegram_msg = utilities.catchDebug(mundusfuncs.fetchHelp())

    context.bot.send_message(
        chat_id=update.effective_chat.id, text=(telegram_msg)
    )

# Get Gas


def getGas(update, context):
    gas_result = utilities.catchDebug(mundusfuncs.returnGas())

    context.bot.send_message(
        chat_id=update.effective_chat.id, text=(gas_result))


# Get Homework
def getHomework(update, context):

    telegram_msg = utilities.catchDebug(mundusfuncs.getHwk(db_connection))

    context.bot.send_message(
        chat_id=update.effective_chat.id, text=(telegram_msg)
    )


def getUserlvl(update, context):

    if context.args == []:
        username = utilities.formatUserName(update)
    else:
        username = context.args[0]

    telegram_msg = utilities.catchDebug(
        mundusfuncs.getLevel(username, db_connection))

    context.bot.send_message(
        chat_id=update.effective_chat.id, text=(telegram_msg)
    )


# Unknown Command
def unknownCmd(update, context):
    response = 'Sorry, I didn\'t understand that command. Try /help to see a list of commands'

    update.message.reply_text(text=response)


# ===== Admin Commands ===== #


def displayAllUsers(update, context):

    username = utilities.formatUserName(update)

    list_of_users = utilities.catchDebug(
        mundusfuncs.displayAll(username, db_connection))

    context.bot.send_message(
        chat_id=update.effective_chat.id, text=(list_of_users)
    )


def setHomework(update, context):

    username = utilities.formatUserName(update)

    telegram_msg = utilities.catchDebug(
        mundusfuncs.setHwk(username, context.args, db_connection))

    context.bot.send_message(
        chat_id=update.effective_chat.id, text=(telegram_msg)
    )


def setUserlvl(update, context):

    username = utilities.formatUserName(update)

    telegram_msg = utilities.catchDebug(
        mundusfuncs.setLevel(username, context.args, db_connection))

    context.bot.send_message(
        chat_id=update.effective_chat.id, text=(telegram_msg)
    )


# ===== Handlers ===== #
# Command Dictionary is always filled with default commands
command_dict = {
    'getuser': getUser,
    'adduser': addUser,
    'updateurl': addInfo,
    'setstatus': updateStatus,
    'getstatus': getStatus,
    'displayallusers': displayAllUsers,
    'help': getHelp,
    'gas': getGas,
    'sethwk': setHomework,
    'gethwk': getHomework,
    'getlevel': getUserlvl,
    'setlevel': setUserlvl
}
# Pulls the custom functions written by the user in ./lib/custom.py
if (utilities.returnSetting('custom_functions')):
    for key in custom.custom_cmds:
        command_dict[key] = custom.custom_cmds[key]

# Dispatch all commands found in the dictionary
for key in command_dict:
    try:
        print(f'Passing {key} to dispatcher')
        cmd = CommandHandler(key, command_dict[key])
        dispatcher.add_handler(cmd)
    except Exception as e:
        print(f'Something happened!{e}')

# Dispatch misc cmd handler seperately
dispatcher.add_handler(MessageHandler(Filters.command, unknownCmd))

# End of Line
updater.start_polling()
