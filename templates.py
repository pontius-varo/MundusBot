responses = {'FORIEGNER': '%s\nStanding with Mundus: Foriegner\nStep it up m8 and start eating, lifting, and programming!', 
            'PLEB' : '%s\nStanding with Mundus: Pleb\nGithub: %s\nWhat a pleb, get gud m8.', 
            'EQUESTRIAN' : '%s\nStanding with Mundus: Equestrian\nGithub: %s\nLinkedIn: %s\nSeems like you\'re getting there, keep it up!', 
            'PATRICIAN' : '%s\nStanding with Mundus: Patrician\nGithub: %s\nLinkedIn: %s\nWebsite: %s\nA true Patrician, 1337 in every way.',
            'SPECIAL': '%s\nStanding with Mundus: Princeps\nGithub: %s\nLinkedIn: %s\nWebsite: %s\nMy lord, I am not worthy to be in your presence!',
            'SPECIAL2' : '%s\nStanding with Mundus: Total Pleb\nGithub: %s\nLinkedIn: %s\nWebsite: %s\nВеди себя прилично, плебей',
            'SPECIAL3': '%s\nStanding with Mundus: Dominus\n%s\n%s\n%s\n1337 of 1337s',
            'STATUS': '%s\'s current status: %s'
            }

queries = {"NEWUSER" : "INSERT INTO Userlib VALUES (%s, \'%s\', 'None', 'None', 'None', 'No Status');", 
        'DOESUSEREXIST' : 'select Username from Userlib where Username = \'%s\';', 'ADDURL': 'update Userlib set %s = \'%s\' where Username =\'%s\';',
        'ADDSTATUS':'update Userlib set Status=\'%s\' where Username=\'%s\';', 'GETSTATUS':'select Status from Userlib where Username=\'%s\''} 

catagories = ['github', 'linkedin', 'website']

catagory_pairs = {'github':'Url1', 'linkedin':'Url2', 'website':'Url3'}

help_txt = ['Current commands: /start, /getuser @username, /adduser, /updateurl [type: github, linkedin, website], /updatestatus, /getstatus @username']
