# Sqlite functions for interacting with DB
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
        print("Query executed successfully")
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
        return string.replace(",","").replace("(","").replace(")","").replace("\'", "").replace("[","").replace("]","")
