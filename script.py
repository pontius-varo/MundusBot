# MundusBot script #

# Imports
import utilities, logging, templates
from telegram.ext import CommandHandler, Updater

from random import randint

# Establish connection to db
myconnection = utilities.create_connection("db/neodatabase")

# Updater
# Put the token here.
updater = Updater(token= #token, use_context=True)
dispatcher = updater.dispatcher

# Logging module, to catch errors
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level = logging.INFO)

# Start function that also processes updates
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I am online!")

def getuser(update, context):
    username = context.args
    try:
        tempdata = utilities.cleanstring(str(utilities.execute_read_query(myconnection, ("select Url1, Url2, Url3 from Userlib where Username = \'%s\';" % username[0]))))
        # This should return a clean array!
        userdata = tempdata.split(" ")

        count = 0

        # Check the amount of Nones!
        for x in userdata:

            if(x == "None"):
                count += 1
            else:
                pass

        if(username[0] == "@eatliftprogram"):
            context.bot.send_message(chat_id=update.effective_chat.id, text=(templates.responses['SPECIAL'] % (username[0], userdata[0], userdata[1], userdata[2])))
        elif(username[0] == "@pavlogetsit"):
            context.bot.send_message(chat_id=update.effective_chat.id, text=(templates.responses['SPECIAL2'] % (username[0], userdata[0], userdata[1], userdata[2])))

        elif(username[0] == "@aurelianus_varo"):
            context.bot.send_message(chat_id=update.effective_chat.id, text=(templates.responses['SPECIAL3'] % (username[0], userdata[0], userdata[1], userdata[2])))

        elif(count > 2):
            context.bot.send_message(chat_id=update.effective_chat.id, text=(templates.responses['FORIEGNER'] % (username[0])))

        elif(count == 2):
            msg = (templates.responses['PLEB'] % (username[0], userdata[0]))
            context.bot.send_message(chat_id=update.effective_chat.id, text=(msg))

        elif(count == 1):
            msg = (templates.reponses['EQUESTRIAN'] % (username[0], userdata[0], userdata[1]))
            context.bot.send_message(chat_id=update.effective_chat.id, text=(msg))

        else:
            msg = (templates.responses['PATRICIAN'] % (username[0], userdata[0], userdata[1], userdata[2]))
            context.bot.send_message(chat_id=update.effective_chat.id, text=(msg))

    except:
        context.bot.send_message(chat_id=update.effective_chat.id, text='Not Found. That user doesn\'t exist m8.')

# Add user to db and returns whether or not it was successful
def adduser(update, context):
    #username = context.args
    #usr = username[0]
    usr = ('@%s' % (update.message.from_user.username))
    if(str(utilities.execute_read_query(myconnection, (templates.queries['DOESUSEREXIST'] % (usr)))) == "[]"):
        # Hardcoded I know, but it works
        userint = randint(1, 10000)
        try:
             utilities.execute_query(myconnection, (templates.queries['NEWUSER'] % (str(userint), usr)))
             context.bot.send_message(chat_id=update.effective_chat.id, text=("%s added successfully to the database." % usr))
        except:
            context.bot.send_message(chat_id=update.effective_chat.id, text=f'Error')
    else:
       context.bot.send_message(chat_id=update.effective_chat.id, text=('That user already exists m8.'))

def addinfo(update, context):
    username = ('@%s' % (update.message.from_user.username))
    entry_type = context.args[0]
    url = context.args[1]

    if entry_type not in templates.catagories:
        context.bot.send_message(chat_id=update.effective_chat.id, text=('Invalid catagory m8.'))
        return

    if(utilities.cleanstring(str((utilities.execute_read_query(myconnection, (templates.queries['DOESUSEREXIST'] % (username)))))) == username):
        try:
            utilities.execute_query(myconnection, (templates.queries['ADDURL'] % (templates.catagory_pairs[entry_type], url, username)))
            context.bot.send_message(chat_id=update.effective_chat.id, text=('Your %s url has been updated, %s' % (entry_type, username)))
        except:
            context.bot.send_message(chat_id=update.effective_chat.id, text='Error')
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text=('You\'re not in my datalibrary, GTFO.'))

# Update Status [Adds a string to the 'status' column in the main table]
def updatestatus(update, context):
    username = ('@%s' % (update.message.from_user.username))
    content = context.args[0]

    if(utilities.cleanstring(str((utilities.execute_read_query(myconnection, (templates.queries['DOESUSEREXIST'] % (username)))))) == username):
        try:
            utilities.execute_query(myconnection, (templates.queries['ADDSTATUS'] % (content, username)))
            context.bot.send_message(chat_id=update.effective_chat.id, text=('Your status has been set, %s' % (username)))
        except:
            context.bot.send_message(chat_id=update.effective_chat.id, text='Error')
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text=('You\'re not in my datalibrary, GTFO.'))

# Get User Status from Database
def getstatus(update, context):
    username = context.args[0]
    if(utilities.cleanstring(str((utilities.execute_read_query(myconnection, (templates.queries['DOESUSEREXIST'] % (username)))))) == username):
        try:
            status = utilities.cleanstring(str(utilities.execute_read_query(myconnection, (templates.queries['GETSTATUS'] % (username)))))
            context.bot.send_message(chat_id=update.effective_chat.id, text=('%s\'s current status: %s' % (username, status)))
        except:
            context.bot.send_message(chat_id=update.effective_chat.id, text='Error')
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text=('That user doesn\'t exist m8'))

# Help
def gethelp(update, context):
    try:
        context.bot.send_message(chat_id=update.effective_chat.id, text=(templates.help_txt[0]))
    except:
        print('Error')

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
addinfo_handler = CommandHandler('updateurl', addinfo, pass_args=True)
dispatcher.add_handler(addinfo_handler)

#  Update Status Handler
update_handler = CommandHandler('updatestatus', updatestatus)
dispatcher.add_handler(update_handler)

# Get Status Handler
get_handler = CommandHandler('getstatus', getstatus)
dispatcher.add_handler(get_handler)

# Help Handler
help_handler = CommandHandler('help', gethelp)
dispatcher.add_handler(help_handler)

# End of Line
updater.start_polling()
