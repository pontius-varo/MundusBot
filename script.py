# MundusBot script #
version = 1.2 #MELTY
# Imports
import utilities, logging, templates
from telegram.ext import CommandHandler, Updater

from random import randint

# Establish connection to db
myconnection = utilities.create_connection("db/neodatabase")

# Updater
# Put the token here.
token='dummy'
updater = Updater(token, use_context=True)
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
            context.bot.send_message(chat_id=update.effective_chat.id, text=(templates.user_res['SPECIAL'] % (username[0], userdata[0], userdata[1], userdata[2])))
        elif(username[0] == "@pavlogetsit"):
            context.bot.send_message(chat_id=update.effective_chat.id, text=(templates.user_res['SPECIAL2'] % (username[0], userdata[0], userdata[1], userdata[2])))

        elif(username[0] == "@aurelianus_varo"):
            context.bot.send_message(chat_id=update.effective_chat.id, text=(templates.user_res['SPECIAL3'] % (username[0], userdata[0], userdata[1], userdata[2])))

        elif(count > 2):
            context.bot.send_message(chat_id=update.effective_chat.id, text=(templates.user_res['FORIEGNER'] % (username[0])))

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
    content = ' '.join(context.args)

    #for x in range(len(context.args)):
        #content += context.args[x]

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

# Sam Saying Yes #
def samsayingyes(update, context):
    sticker = 'CAACAgEAAxkBAAEDMilhftTjxn88VqCiCqYhGh0XxD8T9AACIAIAAjzdyEe2g_Klt73eNCEE'
    chat_id = update.effective_chat.id
    context.bot.send_sticker(chat_id, sticker)

# Thanks #
def greeting(update, context):
    key = randint(0, len(templates.responses) - 1)
    update.message.reply_text(text=templates.responses[key])

# Cells #
def showcells(update, context):
    usernum = context.args[0]

    try:
        int(usernum)
    except:
        update.message.reply_text(text='That isn\'t an interger m8')
        return

    if(int(usernum) > 30):
        update.message.reply_text(text='Too long! Use an interger under 30 please.')
        return

    num = 0
    msg = ''
    while num < int(usernum):
        msg += ('\n%s' % (templates.text[0]))
        num += 1

    context.bot.send_message(chat_id=update.effective_chat.id, text=(msg))
# ===== Admin Commands ===== #

def displayallusers(update, context):
    username = ('@%s' % (update.message.from_user.username))
    admin = False

    for x in range(len(templates.admins)):

        if (username == templates.admins[x]):
            admin = True
        else:
            print('Nope')

    if(admin == True):
        try:
            data_1 = utilities.execute_read_query(myconnection, (templates.queries['ALLUSERS']))
            data_2 = utilities.execute_read_query(myconnection, (templates.queries['ALLSTATUS']))

            users = utilities.cleanarray(data_1)
            userstatus = utilities.cleanarray(data_2)

            msg = ('Current Number of Users in My DB: %s\nUsers with Status:' % (len(users)))

            for x in range(len(users)):
                msg += ('\n%s | %s' % (users[x], userstatus[x]))

            context.bot.send_message(chat_id=update.effective_chat.id, text=(msg))
        except:
            print('ERROR| PLEASE DEBUG')
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text=('You\'re not an admin, GTFO n00b'))

# ===== Handlers ===== #

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

#Display All Users Handler #
dau_handler = CommandHandler('displayallusers', displayallusers)
dispatcher.add_handler(dau_handler)

# Sam Saying Yes [CUSTOM]#
sam_yes = CommandHandler('samsayingyes', samsayingyes)
dispatcher.add_handler(sam_yes)

# Cells #
cells = CommandHandler('cells', showcells, pass_args=True)
dispatcher.add_handler(cells)

# Greeting #
mund_greeting = CommandHandler('thanks', greeting)
dispatcher.add_handler(mund_greeting)

# End of Line
updater.start_polling()
