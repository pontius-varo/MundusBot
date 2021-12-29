# MundusBot

Latest Version: 2.0 "BLOOD"

A telegram bot written in Python 3.9 for a private server, but can now be used anywhere (if your sql db aligns with Mundus' queries).

Please test out functionality by running nirntests.py, as this will tell you whether or not your settings are configured correctly
and if everything is in place.

Requires the following libraries: sqlite3, python-telegram-bot

#Change Log#
1.2 Added /displayallusers, /samsayingyes, /cells, and /thanks along with admin array and empty token variable.
1.3 Fixed bug within /updatestatus and /displayallusers
1.5 Fixed more bugs in /getuser

# 2.0 'BLOOD' Changelog
* Cleaned up code (script.py < 160 lines)
* Added a settings.json file for customization
* Added lib/custom.py file for custom commands
* Added lib/mundusfuncs.py for vanilla commands
* Moved utilities.py, templates.py, pygas.py to lib directory
* Created Unit testing for Mundus (nirntests.py)
* Added a function to catch unknown commands (unknownCmd)
* Added a function to check the validity of a username (isUserValid)
* Added a function to 'clean' username retrieved from telegram (formatUserName)
* Added a function that returns the current ETH gas price (getGas)
* Reworked previous vanilla command functions
* Added functions to return values from settings.json (getAdmins, getSetting)
* Added error handling (Basic, Mundus will return errors to the user)
* Removed greeting() and cells() for the time being
* Changed Default Mundus Photo on Telegram
