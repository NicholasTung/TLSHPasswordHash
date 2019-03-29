import string
import pandas as pd
import secrets
import csv 

def toggleCapitalization(pw):
    if pw.isupper():
        return pw.lower()
    else:
        return pw.upper()

csvinput = pd.read_csv('randomlyGeneratedPasswords.csv')

twoSubstitution = list()
twoInsertion = list()
twoDeletion = list()
twoCapMistake = list()
subPunctuation = list()

specialChars = list(string.punctuation)
specialChars.remove(",")

allChars = string.ascii_uppercase + string.ascii_lowercase + string.digits + ''.join(specialChars)

for password in csvinput['Password']:

    firstInsert = secrets.randbelow(len(password))
    while True:
        secondInsert = secrets.randbelow(len(password))
        if secondInsert == firstInsert:
            secondInsert = secrets.randbelow(len(password))
        else:
            break

    twoInsertion.append([password[:min(firstInsert, secondInsert)] + secrets.choice(allChars) + password[min(firstInsert, secondInsert):max(firstInsert, secondInsert)]
                         + secrets.choice(allChars) + password[max(firstInsert, secondInsert):]])
    
#########################################################################################################
    firstDelete = secrets.randbelow(len(password))
    while True:
        secondDelete = secrets.randbelow(len(password))
        if secondDelete == firstDelete:
            secondDelete = secrets.randbelow(len(password))
        else:
            break
    twoDeletion.append([password[:min(firstDelete, secondDelete)] + password[min(firstDelete, secondDelete) + 1:max(firstDelete, secondDelete)]
                         + password[max(firstDelete, secondDelete) + 1:]])
    
#########################################################################################################
    firstSub = secrets.randbelow(len(password))
    while True:
        secondSub = secrets.randbelow(len(password))
        if secondSub == firstSub:
            secondSub = secrets.randbelow(len(password))
        else:
            break
    twoSubstitution.append([password[:min(firstSub, secondSub)] + secrets.choice(allChars) + password[min(firstSub, secondSub) + 1:max(firstSub, secondSub)]
                         + secrets.choice(allChars) + password[max(firstSub, secondSub) + 1:]])
    
#########################################################################################################
    firstCap = secrets.randbelow(len(password))
    while True:
        secondCap = secrets.randbelow(len(password))
        if secondCap == firstCap:
            secondCap = secrets.randbelow(len(password))
        else:
            break
    while True:
        if password[firstCap] in string.ascii_letters and password[secondCap] in string.ascii_letters:
            twoCapMistake.append([password[:min(firstCap, secondCap)] + toggleCapitalization(password[firstCap] + password[min(firstCap, secondCap) + 1:max(firstCap, secondCap)])
                                 + toggleCapitalization(password[secondCap]) + password[min(firstCap, secondCap) + 1:]])
            
            break
        else:
            if password[firstCap] not in string.ascii_letters:
                firstCap = secrets.randbelow(len(password))
            elif password[secondCap] not in string.ascii_letters:
                secondCap = secrets.randbelow(len(password))
#########################################################################################################
    firstSubPunc = secrets.randbelow(len(password))
    while True:
        secondSubPunc = secrets.randbelow(len(password))
        if secondSubPunc == firstSubPunc:
            secondSubPunc = secrets.randbelow(len(password))
        else:
            break
    while True:
        if password[firstSubPunc] in string.punctuation and password[secondSubPunc] in string.punctuation:
            subPunctuation.append([password[:min(firstSubPunc, secondSubPunc)] + secrets.choice(string.ascii_letters) + password[(min(firstSubPunc, secondSubPunc) + 1):max(firstSubPunc, secondSubPunc)]
                                  + secrets.choice(string.ascii_letters) + password[max(firstSubPunc, secondSubPunc) + 1:]])
            
            break
        else:
            if password[firstSubPunc] not in string.punctuation:
                firstSubPunc = secrets.randbelow(len(password))
            elif password[secondSubPunc] not in string.punctuation:
                secondSubPunc = secrets.randbelow(len(password))

#########################################################################################################

csvinput['twoSubstitution'] = twoSubstitution
csvinput['twoSubstitution'] = csvinput['twoSubstitution'].apply(' '.join)

csvinput['twoInsertion'] = twoInsertion
csvinput['twoInsertion'] = csvinput['twoInsertion'].apply(' '.join)

csvinput['twoDeletion'] = twoDeletion
csvinput['twoDeletion'] = csvinput['twoDeletion'].apply(' '.join)

csvinput['twoCapMistake'] = twoCapMistake
csvinput['twoCapMistake'] = csvinput['twoCapMistake'].apply(' '.join)

csvinput['subPunctuation'] = subPunctuation
csvinput['subPunctuation'] = csvinput['subPunctuation'].apply(' '.join)

csvinput.to_csv("randomlyGeneratedPasswords.csv", index = False, quoting = csv.QUOTE_ALL)

