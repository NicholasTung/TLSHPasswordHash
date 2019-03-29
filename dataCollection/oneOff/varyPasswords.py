import string
import pandas as pd
import secrets
import csv 

csvinput = pd.read_csv('randomlyGeneratedPasswords.csv')

oneSubstitution = list()
oneInsertion = list()
oneDeletion = list()
oneCapMistake = list()
subPunctuation = list()

specialChars = list(string.punctuation)
specialChars.remove(",")

allChars = string.ascii_uppercase + string.ascii_lowercase + string.digits + ''.join(specialChars)

for password in csvinput['Password']:

    insert = secrets.randbelow(len(password))
    oneInsertion.append([password[:insert] + secrets.choice(allChars) + password[insert:]])

    delete = secrets.randbelow(len(password))
    oneDeletion.append([password[:delete] + password[(delete + 1):]])

    sub = secrets.randbelow(len(password))
    oneSubstitution.append([password[:sub] + secrets.choice(allChars) + password[(sub + 1):]])

    cap = secrets.randbelow(len(password))
    while True:
    	if password[cap] in string.ascii_letters:
    		if password[cap].isupper() is True:
    			oneCapMistake.append([password[:cap] + password[cap].lower() + password[(cap + 1):]])
    		else:
    			oneCapMistake.append([password[:cap] + password[cap].upper() + password[(cap + 1):]])

    		break
    	else:
    		cap = secrets.randbelow(len(password))

    subPunc = secrets.randbelow(len(password))
    while True:
    	if password[subPunc] in string.punctuation:
    		subPunctuation.append([password[:sub] + secrets.choice(string.ascii_letters) + password[(sub + 1):]])

    		break
    	else:
    		subPunc = secrets.randbelow(len(password))



csvinput['oneSubstitution'] = oneSubstitution
csvinput['oneSubstitution'] = csvinput['oneSubstitution'].apply(' '.join)

csvinput['oneInsertion'] = oneInsertion
csvinput['oneInsertion'] = csvinput['oneInsertion'].apply(' '.join)

csvinput['oneDeletion'] = oneDeletion
csvinput['oneDeletion'] = csvinput['oneDeletion'].apply(' '.join)

csvinput['oneCapMistake'] = oneCapMistake
csvinput['oneCapMistake'] = csvinput['oneCapMistake'].apply(' '.join)

csvinput['subPunctuation'] = subPunctuation
csvinput['subPunctuation'] = csvinput['subPunctuation'].apply(' '.join)

csvinput.to_csv("randomlyGeneratedPasswords.csv", index = False, quoting = csv.QUOTE_ALL)

