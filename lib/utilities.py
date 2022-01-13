# Sqlite functions for interacting with DB
# from pathlib import Path
import json
from sqlite3 import Error, connect


def create_connection(path):
    connection = None
    try:
        connection = connect(path, check_same_thread=False)
        print("Connection to DB established.")
    except Error as e:
        print(f'The error\'{e}\' occurred. Are you sure db file exists?')

    return connection


def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
    except Error as e:
        print(f"An error occured: \'{e}\'")


def execute_read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"The error '{e}' occured")

# Other functions


def newarray(array):
    x = 1
    newarray = []
    while x < len(array):
        newarray.append(array[x])
        x += 1
    return newarray


def tostring(array):
    tempstring = ' '
    return tempstring.join(array)


def cleanstring(string):
    return string.replace(",", "").replace("(", "").replace(")", "").replace("\'", "").replace("[", "").replace("]", "")


def cleanarray(array):
    for x in range(len(array)):
        array[x] = cleanstring(str(array[x]))
    return array


def formatUserName(data):
    user_raw = data.message.from_user.username
    return f'@{user_raw}'


# These functions read the settings.json file. Change at your own discretion
def getAdmins():
    try:
        file = open('./settings.json')
        settings = json.load(file)
        file.close()

        admin_list = []

        # First Add the Owner
        admin_list.append(settings['server_owner'])

        for admin in settings['server_admins']:
            admin_list.append(admin)

        return admin_list

    except Exception as e:
        return [f'Something happened: {e}', 0]


def getOwner():
    try:
        file = open('./settings.json')
        settings = json.load(file)
        file.close()

        return [settings['server_owner'], 1]

    except Exception as e:
        return [f'Something happened: {e}', 0]


def returnSetting(setting):
    try:
        file = open('./settings.json')
        settings = json.load(file)
        file.close()

        return settings[setting]

    except Exception as e:
        return [f'Unable to return {setting}: {e}', 0]


def catchDebug(msg):
    if(msg[1]):
        return msg[0]
    else:
        return 'Oops, something happened. Are you in the db? Ping the Admin for details.'
