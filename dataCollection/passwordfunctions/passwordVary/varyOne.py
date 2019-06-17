import string
import secrets
from . import charsets

allChars = charsets.allChars

def insertOne(password):
    insert = secrets.randbelow(len(password))
    result = password[:insert] + secrets.choice(allChars) + password[insert:]
    return result

def substituteOne(password):
    delete = secrets.randbelow(len(password))
    return password[:delete] + password[(delete + 1):]

def deleteOne(password):
    sub = secrets.randbelow(len(password))
    return password[:sub] + secrets.choice(allChars) + password[(sub + 1):]

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


