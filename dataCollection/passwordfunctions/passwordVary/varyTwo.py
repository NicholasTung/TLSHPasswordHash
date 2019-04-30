import string
import secrets
from . import charsets

allChars = charsets.allChars
def toggleCapitalization(pw):
    if pw.isupper():
        return pw.lower()
    else:
        return pw.upper()

def insertTwo(password):
    firstInsert = secrets.randbelow(len(password))
    while True:
        secondInsert = secrets.randbelow(len(password))
        if secondInsert == firstInsert:
            secondInsert = secrets.randbelow(len(password))
        else:
            break

    return password[:min(firstInsert, secondInsert)] + secrets.choice(allChars)\
                    + password[min(firstInsert, secondInsert):max(firstInsert, secondInsert)]\
                    + secrets.choice(allChars) + password[max(firstInsert, secondInsert):]

def substituteTwo(password):
    firstSub = secrets.randbelow(len(password))
    while True:
        secondSub = secrets.randbelow(len(password))
        if secondSub == firstSub:
            secondSub = secrets.randbelow(len(password))
        else:
            break
    return password[:min(firstSub, secondSub)] + secrets.choice(allChars)\
                    + password[min(firstSub, secondSub) + 1:max(firstSub, secondSub)]\
                    + secrets.choice(allChars) + password[max(firstSub, secondSub) + 1:]

def deleteTwo(password):
    firstDelete = secrets.randbelow(len(password))
    while True:
        secondDelete = secrets.randbelow(len(password))
        if secondDelete == firstDelete:
            secondDelete = secrets.randbelow(len(password))
        else:
            break
    return password[:min(firstDelete, secondDelete)]+ password[min(firstDelete, secondDelete)\
                    + 1:max(firstDelete, secondDelete)]\
                    + password[max(firstDelete, secondDelete) + 1:]

def capitalizeTwo(password):
    firstCap = secrets.randbelow(len(password))
    while True:
        secondCap = secrets.randbelow(len(password))
        if secondCap == firstCap:
            secondCap = secrets.randbelow(len(password))
        else:
            break
    while True:
        if password[firstCap] in string.ascii_letters and password[secondCap] in string.ascii_letters:
            return password[:min(firstCap, secondCap)] + toggleCapitalization(password[firstCap]\
                            + password[min(firstCap, secondCap) + 1:max(firstCap, secondCap)])\
                            + toggleCapitalization(password[secondCap]) + password[max(firstCap, secondCap) + 1:]
            
            break
        else:
            if password[firstCap] not in string.ascii_letters:
                firstCap = secrets.randbelow(len(password))
            elif password[secondCap] not in string.ascii_letters:
                secondCap = secrets.randbelow(len(password))