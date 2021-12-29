from random import randint
import unittest
from lib import utilities
from lib import mundusfuncs

test_connection = utilities.create_connection("db/neodatabase")


class NirnTest(unittest.TestCase):

    def test_isTokenAvailable(self):
        token = utilities.returnSetting('server_token')

        self.assertTrue(token[1], token[0])

    # The functions within SCRIPT.PY need to be rewritten in order to return
    # values that can be tested using the NirnTest object

    # Function for GetUser
    def test_getUserTest(self):
        # Testing username saved in every database
        username = '@nirnbot'
        # Check if the query is executed successfully
        result = mundusfuncs.getUserInfo(username, test_connection)
        self.assertTrue(result[1], result[0])

    # Function for AddUser
    def test_addUserTest(self):
        # Dummy username
        username = '@anoymous' + str(randint(1, 1000))
        # Get the result
        result = mundusfuncs.addUsertoDb(username, test_connection)
        # Test the result
        self.assertTrue(result[1], result[0])
    # Function for Add Info

    def test_addDataTest(self):
        # Dummy username
        username = '@nirnbot'

        result = mundusfuncs.addData(
            username, ['website', 'https://dummy.org/'], test_connection)

        self.assertTrue(result[1], result[0])

    # Function for UpdateStatus
    def test_updateStatusTest(self):
        # Dummy username
        username = '@nirnbot'

        result = mundusfuncs.updateUserStatus(
            username, 'Testing...', test_connection)

        self.assertTrue(result[1], result[0])

    # Function for Get Status
    def test_getStatusTest(self):
        # Dummy Username
        username = '@nirnbot'

        result = mundusfuncs.getUserStatus(username, test_connection)

        self.assertTrue(result[1], result[0])

    # Function for Get Gas
    def test_getGas(self):
        result = mundusfuncs.returnGas()

        self.assertTrue(result[1], result[0])

    # Function for Display All Users
    def test_firstAdmin(self):
        # Dummy usernamer, should return false
        username = '@nirnbot'
        result = mundusfuncs.displayAll(username, test_connection)

        self.assertFalse(result[1], result[0])

    # Consider the following file structure
    # main.py (compiles bot), commands.py (contains all functions),
    # library.py (contains strings and arrays), utilities.py ->
    # (contains auxiliary functions), gas.py (standalone for pygas),
    # settings.json (user settings for bot), start.py ->
    # allow first time user to add token and database values, while
    # saving those values in the settings.json file for later use
    # first time execution should be as follows:
    # start.py -> (rewrites) settings.json, main.py -> (triggers nirntest.py)
    # nirntest.py (if successful) -> (takes data from) settings.json ->
    # main.py is compiled and the bot is run successfully


if __name__ == '__main__':
    unittest.main()
