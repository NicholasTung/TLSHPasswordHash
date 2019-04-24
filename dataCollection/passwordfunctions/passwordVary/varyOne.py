import string
import secrets
import charsets

def insertOne(password):
	insert = secrets.randbelow(len(password))
    return password[:insert] + secrets.choice(charsets.allChars) + password[insert:]

def substituteOne(password):
	delete = secrets.randbelow(len(password))
    return password[:delete] + password[(delete + 1):]

def deleteOne(password):
	sub = secrets.randbelow(len(password))
    return password[:sub] + secrets.choice(charsets.allChars) + password[(sub + 1):]

def capitalizeOne(password):
	cap = secrets.randbelow(len(password))
    while True:
    	if password[cap] in string.ascii_letters:
    		if password[cap].isupper() is True:
    			return password[:cap] + password[cap].lower() + password[(cap + 1):]
    		else:
    			return password[:cap] + password[cap].upper() + password[(cap + 1):]

    		break
    	else:
    		cap = secrets.randbelow(len(password))


