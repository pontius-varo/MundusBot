# MundusBot script #

# Imports
import utilities, logging
from telegram.ext import CommandHandler, Updater

# Establish connection to db
myconnection = utilities.create_connection("db/database.db")

# Updater
updater = Updater(token='1932470254:AAF2Xtxpgu0k_NkIAcIOkuVVsTT3i5Nb744', use_context=True)
dispatcher = updater.dispatcher

# Logging module, to catch errors
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level = logging.INFO)

# Start function that also processes updates
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Et tu, Josh?")

def getuser(update, context):
    username = context.args
    try:
        usrinfo = utilities.cleanstring(str(utilities.execute_read_query(myconnection, ("select url1 from main where user=\'%s\'" % username[0]))))
        context.bot.send_message(chat_id=update.effective_chat.id, text=('%s\n%s' % (username[0], usrinfo)))

    except:
        context.bot.send_message(chat_id=update.effective_chat.id, text='Not found')
        print("User not found, are you sure it exists?")

# Add user to db and returns whether or not it was successful
def adduser(update, context):
    username = context.args
    usr = username[0]
    #if(execute_read_query(myconnection, ("select user from main where user=%s"% username[0]))):
    #       context.bot.send_message(chat_id=update.effective_chat.id, text=('Duplicate username detected!'))
    #else:
    try:
        utilities.execute_query(myconnection, ("insert into main(user) values (\'%s\');" % usr))
    except:
        context.bot.send_message(chat_id=update.effective_chat.id, text=f'Error:{e}')

    context.bot.send_message(chat_id=update.effective_chat.id, text=("%s added successfully to the database. Boom baby!" % username[0]))

# Add URL/information to db
def addinfo(update, context):
    username = context.args[0]
    url = context.args[1]
    # Put code to check for dupes here!
    try:
        utilities.execute_query(myconnection, ("update main set url1=(\'%s\') where user=\'%s\'" % (url, username)))
        context.bot.send_message(chat_id=update.effective_chat.id, text=('%s\'s url was successfully added to the database.' % username))
    except:
        context.bot.send_message(chat_id=update.effective_chat.id, text='Error: {e}')
        print('You might want to fix this!')

# Update Status [Adds a string to the 'status' column in the main table]
def updatestatus(update, context):
    username = context.args[0]
    status_str = utilities.tostring(utilities.newarray(context.args))
    try:
        utilities.execute_query(myconnection, ("update main set status=(\'%s\') where user=\'%s\'" %(status_str, username)))
    except:
        context.bot.send_message(chat_id=update.effective_chat.id, text='An error occured')
        print("An error occured")

    context.bot.send_message(chat_id=update.effective_chat.id, text='Your status has been set.')

def getstatus(update, context):
    username = context.args
    try:
        mystatus = utilities.cleanstring(str(utilities.execute_read_query(myconnection, ("select status from main where user=\'%s\'" % username[0]))))
    except:
        context.bot.send_message(chat_id=update.effective_chat.id, text='An error occured')
        print("An error occured")

    context.bot.send_message(chat_id=update.effective_chat.id, text=('%s\'s status:\n%s' % (username[0], mystatus)))

# Handlers #

# Start Handler
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)
# Get_User Handler
get_userhandler = CommandHandler('getuser', getuser, pass_args=True)
dispatcher.add_handler(get_userhandler)
# Add User Handler
adduser_handler = CommandHandler('adduser', adduser, pass_args=True)
dispatcher.add_handler(adduser_handler)
# Add Info Handler
addinfo_handler = CommandHandler('addinfo', addinfo, pass_args=True)
dispatcher.add_handler(addinfo_handler)

#  Update Status Handler
update_handler = CommandHandler('updatestatus', updatestatus)
dispatcher.add_handler(update_handler)

# Get Status Handler
get_handler = CommandHandler('getstatus', getstatus)
dispatcher.add_handler(get_handler)

# End of Line
updater.start_polling()
