from . import templates
from . import utilities
from . import pythongas
from datetime import date
from random import randint


def isUserValid(username, connection):
    try:
        userquery = utilities.execute_read_query(
            connection,
            f'select Username from Userlib where Username=\'{username}\'')

        # ftfy
        if (userquery != '' and userquery != []):
            return True
        else:
            return False

    except Exception as e:
        return [f'Something happened: {e}', 0]

# Returns User Information from the DB


def getUserInfo(username, connection):

    count = 0

    valid = isUserValid(username, connection)

    if(valid):
        try:
            initial_data = utilities.execute_read_query(
                connection, (templates.queries['GETUSER'] % username))

            userdata = list(initial_data[0])

        except Exception as e:
            return [f'Error: {e}', 0]
    else:
        return ["Username is not Valid. Are you registered in the DB?", 0]

    admin_list = utilities.getAdmins()
    special_list = utilities.returnSetting('server_wizards')

    try:
        for entry in userdata:
            if(entry == "None"):
                count += 1
        # Compare username to values in admin_list and special_list

        if username == admin_list[0]:
            msg = templates.user_res['SPECIAL'] % (
                username, userdata[0], userdata[1], userdata[2])

        elif username in admin_list:
            msg = templates.user_res['SPECIAL3'] % (
                username, userdata[0], userdata[1], userdata[2]
            )

        elif username in special_list:
            msg = templates.user_res['SPECIAL4'] % (
                username, userdata[0], userdata[1], userdata[2]
                )
        # Else, username is most likely normal so return appropriate string
        else:
            if(count > 2):
                msg = templates.user_res['FORIEGNER'] % (username)
            elif(count == 2):
                msg = (templates.user_res['PLEB'] % (username, userdata[0]))
            elif(count == 1):
                msg = (templates.user_res['EQUESTRIAN'] %
                       (username, userdata[0], userdata[1]))
            else:
                msg = (templates.user_res['PATRICIAN'] % (
                    username, userdata[0], userdata[1], userdata[2]))

        return [msg, 1]
    except Exception as e:
        return [f'An error occured when organzing the string data: {e}', 0]


# Adds User to the DB
def addUsertoDb(username, connection):
    # Check to see if the username exists in the database
    try:
        if(str(utilities.execute_read_query(connection, (templates.queries['DOESUSEREXIST'] % (username)))) == "[]"):
            userint = randint(1, 10000)
    # If it does, return a string and false in an array
    except Exception:
        return ['That user already exits', 0]
    # if not, try and add the user to the database
    try:
        utilities.execute_query(connection,
                                (templates.queries['NEWUSER'] % (str(userint),
                                                                 username)))
        return [f'{username} was successfully added to the database', 1]
    except Exception as e:
        return [f'An error occured: {e}', 0]


def addData(username, data, connection):

    valid = isUserValid(username, connection)

    if(valid):
        if(data[0] in templates.categories):
            try:
                utilities.execute_query(
                    connection, f'update Userlib set {templates.category_pairs[data[0]]} = \'{data[1]}\' where Username =\'{username}\';')
                return [f'Your {data[0]} link has successfully been added, {username}', 1]
            except Exception as e:
                return [f'Something happened: {e}', 0]
        else:
            return [f'This category \'{data[0]}\' is not valid.', 0]
    else:
        return [f'Username {username} is not valid. Is the User in the DB?', 0]


def updateUserStatus(username, data, connection):

    valid = isUserValid(username, connection)
    usercontent = ' '.join(data)

    if(valid):
        try:
            utilities.execute_query(
                connection, f'update Userlib set Status=\'{usercontent}\' where Username=\'{username}\';')
            return [f'Your status has been set, {username}!', 1]
        except Exception as e:
            return [f'Something happened: {e}', 0]
    else:
        return [f'Username {username} is not valid. Are you in the db?', 0]


def checkData(update, data):
    # Assuming it's an array
    if data == []:
        return ('@%s' % (update.message.from_user.username))
    else:
        return data.args[0]


def getUserStatus(username, connection):

    valid = isUserValid(username, connection)

    if(valid):
        try:
            # This is a tuple
            raw_status = utilities.execute_read_query(
                connection, f'select Status from Userlib where Username=\'{username}\';')

            status = ''.join(raw_status[0])

            return [f'{username}\'s current status:\n{status}', 1]
        except Exception as e:
            return [f'Something happened: {e}', 0]
    else:
        return [f'Username {username} is not valid. Are you in the db?', 0]


def fetchHelp():
    try:
        return [templates.help_txt[0], 1]
    except Exception as e:
        return [f'{e}', 0]


def returnGas():
    try:
        gas_result = pythongas.gas()
        return [gas_result, 1]
    except Exception as e:
        return [f'{e}', 0]


def getHwk(connection):
    try:
        raw_data = utilities.execute_read_query(
            connection, 'select hwkStr from Homework where id=(select max(id) from Homework);')

        hwk = ''.join(raw_data[0])

        return [hwk, 1]

    except Exception as e:
        return [f'Something happened: {e}', 0]


def getLevel(username, connection):
    valid = isUserValid(username, connection)

    if(valid):
        try:
            raw_data = utilities.execute_read_query(
                connection, f'select level from Userlib where Username=\'{username}\';')

            # Catch NONE types, there should be a better way to do this!
            if(raw_data[0][0] == None):
                return [f'Your level hasn\'t been set yet, {username}', 1]

            userlevel = " ".join(str(raw_data[0][0]))

            # If it returns nothing, this should catch it.
            if(userlevel != [] and userlevel != ''):
                return [f'{username}\'s level: {userlevel}', 1]
            else:
                return [f'Your level hasn\'t been set yet, {username}', 0]

        except Exception as e:
            return [f'Something happened {e}', 0]

    else:
        return [f'Username {username} is not valid. Is the User in the db?', 0]


# ===== Admin Commands ===== #

def displayAll(username, connection):

    valid = isUserValid(username, connection)

    admin_list = utilities.getAdmins()

    if(valid):
        if(username in admin_list):
            # Proceed with command
            try:
                raw_users = utilities.execute_read_query(
                    connection, templates.queries['ALLUSERS'])
                raw_status = utilities.execute_read_query(
                    connection, templates.queries['ALLSTATUS'])

                users = []
                user_info = []

                usercount = len(raw_users)

                for x in range(usercount):
                    users.append(''.join(raw_users[x]))
                    user_info.append(''.join(raw_status[x]))
                # Create the message listing the users
                msg = f'Current Number of Users in My DB: {usercount}\n'

                # Another interation.....
                for x in range(usercount):
                    msg += ('\n%s | %s' % (users[x], user_info[x]))

                # Return the message
                return [msg, 1]
            except Exception as e:
                return [f'Something happened: {e}', 0]
        else:
            return [f'{username} is not an admin', 0]
    else:
        return [f'Username {username} is not valid. Is the User in the db?', 0]


def setHwk(username, data, connection):
    valid = isUserValid(username, connection)

    today = date.today()

    usercontent = ' '.join(data)

    if(valid):
        owner = utilities.getOwner()[0]
        if(username == owner):

            if(utilities.execute_read_query(connection, f'select date from Homework where date=\'{today}\'') == []):
                # If there is no matching date, create a new one
                try:
                    utilities.execute_query(
                        connection, f'insert into Homework(hwkStr, date) values (\'{usercontent}\', \'{today}\');')

                    return [f'Homework has successfully been added for {date}, {username}!', 1]
                except Exception as e:
                    return [f'Something happened: {e}', 0]
                # Else, just change the entry
            else:
                try:
                    utilities.execute_query(
                        connection, f'update Homework set hwkStr=\'{usercontent}\' where date=\'{today}\';')
                    return [f'Homework for {today} was successfully updated, {username}', 1]
                except Exception as e:
                    return [f'Something happened: {e}', 0]
        else:
            return [f'User {username} is not owner', 0]
    else:
        return [f'Username {username} is not valid. Is the User in the db?', 0]


def setLevel(username, data, connection):
    valid = isUserValid(username, connection)

    # Use userargs as this is more straightforward
    # Need to check first param!
    # userargs = data
    if(valid):
        owner = utilities.getOwner()[0]
        if(username == owner):
            try:
                utilities.execute_query(
                    connection, f'update Userlib set level = {data[1]} where Username =\'{data[0]}\'')

                return [f'Success! {data[0]}\'s level has been updated to {data[1]}, {username}', 1]

            except Exception as e:
                return [f'Something happened: {e}', 0]

        else:
            return [f'User {username} is not owner', 0]
    else:
        return [f'Username {username} is not valid. Is the User in the db?', 0]
