# All of these "Tiers" can be changed at your discretion.
# Just make sure to edit the /getuser function and replace your key strings with my defaults
user_res = {'FORIEGNER': '%s\nStanding with Mundus: Foreigner\nJust Eat Lift Program, bro',
            'PLEB': '%s\nStanding with Mundus: Pleb\nGithub: %s\Get Gud',
            'EQUESTRIAN': '%s\nStanding with Mundus: Equestrian\nGithub: %s\nLinkedIn: %s\nSeems like you\'re getting there, keep it up!',
            'PATRICIAN': '%s\nStanding with Mundus: Patrician\nGithub: %s\nLinkedIn: %s\nWebsite: %s\nA true Patrician.',
            'SPECIAL': '%s\nStanding with Mundus: Princeps\nGithub: %s\nLinkedIn: %s\nWebsite: %s\nMy lord, I am not worthy to be in your presence!',
            'SPECIAL3': '%s\nStanding with Mundus: Scholae\nGithub: %s\nLinkedIn: %s\nWebsite: %s\nConfirmed 1337 H4X0R',
            'SPECIAL4': '%s\nStanding with Mundus: Magus\nGithub: %s\n LinkedIn: %s\nWebsite: %s\n\'And there I saw a mage, whose vast wit and hundred winters are but as the hands of loyal vassals toiling for their liege.\'',
            'STATUS': '%s\'s current status: %s'
            }

queries = {"NEWUSER": "INSERT INTO Userlib VALUES (%s, \'%s\', 'None', 'None', 'None', 'No Status');",
           'DOESUSEREXIST': 'select Username from Userlib where Username = \'%s\';',
           'ADDURL': 'update Userlib set %s = \'%s\' where Username =\'%s\';',
           'ADDSTATUS': 'update Userlib set Status=\'%s\' where Username=\'%s\';',
           'GETSTATUS': 'select Status from Userlib where Username=\'%s\';',
           'ALLUSERS': 'select Username from Userlib;',
           'ALLSTATUS': 'select Status from Userlib;',
           'GETUSER': 'select Url1, Url2, Url3 from Userlib where Username = \'%s\';',
           'GETLEVEL': 'select lvl from Userlib where Username = \'%s\';',
           'UPDATELEVEL': 'update Userlib set lvl=\'%s\' where Username=\'%s\';',
           'SETHOMEWORK': 'INSERT INTO Homework values ()'}

categories = ['github', 'linkedin', 'website']

category_pairs = {'github': 'Url1', 'linkedin': 'Url2', 'website': 'Url3'}

help_txt = ['Commands: /getuser @username, /adduser, /updateurl [type: github, linkedin, website],\n/setstatus, /getstatus @username, /samsayingyes, /gas, /getlevel, /gethwk']

responses = ['You\'re welcome']
