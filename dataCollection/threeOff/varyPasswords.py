import string
import pandas as pd
import secrets
import csv 

def toggleCapitalization(pw):
    if pw.isupper():
        return pw.lower()
    else:
        return pw.upper()

def genThree(pw):
    indices = list()
    i = 0
    while (i < 3):
        index = secrets.randbelow(len(pw))
        if index not in indices:
            indices.append(index)
            i -= -1

    indices.sort()

    return indices

csvinput = pd.read_csv('randomlyGeneratedPasswords.csv')

threeSubstitution = list()
threeInsertion = list()
threeDeletion = list()
threeCapMistake = list()
subPunctuation = list()

specialChars = list(string.punctuation)
specialChars.remove(",")

allChars = string.ascii_uppercase + string.ascii_lowercase + string.digits + ''.join(specialChars)

for password in csvinput['Password']:

    indices = genThree(password)

    threeInsertion.append([password[indices[0]] + secrets.choice(allChars) + password[indices[0] + 1:indices[1]]
                         + secrets.choice(allChars) + password[indices[1]:indices[2]] 
                         + secrets.choice(allChars) + password[indices[2]:]])
    
#########################################################################################################
    indices = genThree(password)
    
    threeDeletion.append([password[:indices[0]] + password[indices[0] + 1:indices[1]]
                         + password[indices[1] + 1:indices[2]] + password[indices[2] + 1:]])
    
#########################################################################################################
    indices = genThree(password)
    
    threeSubstitution.append([password[:indices[0]] + secrets.choice(allChars) + password[indices[0] + 1:indices[1]]
                         + secrets.choice(allChars) + password[indices[1] + 1:indices[2]]
                         + secrets.choice(allChars) + password[indices[2] + 1:]])
    
#########################################################################################################
    indices = genThree(password)
    
    while True:
        if password[indices[0]] in string.ascii_letters and password[indices[1]] in string.ascii_letters and password[indices[2]] in string.ascii_letters:
            threeCapMistake.append([password[:indices[0]] + toggleCapitalization(password[indices[0]]) + password[indices[0] + 1:indices[1]]
                         + toggleCapitalization(password[indices[1]]) + password[indices[1] + 1:indices[2]]
                         + toggleCapitalization(password[indices[2]]) + password[indices[2] + 1:]])
            
            break
        else:
            if password[indices[0]] not in string.ascii_letters:
                indices[0] = secrets.randbelow(len(password))
            elif password[indices[1]] not in string.ascii_letters:
                indices[1] = secrets.randbelow(len(password))
            elif password[indices[2]] not in string.ascii_letters:
                indices[2] = secrets.randbelow(len(password))
#########################################################################################################
    # indices = genThree(password)
    
    # while True:
    #     if password[indices[0]] in string.punctuation and password[indices[1]] in string.punctuation and password[indices[2]] in string.punctuation:
    #         subPunctuation.append([password[:indices[0]] + secrets.choice(string.ascii_letters) + password[indices[0] + 1:indices[1]]
    #                      + secrets.choice(string.ascii_letters) + password[indices[1] + 1:indices[2]]
    #                      + secrets.choice(string.ascii_letters) + password[indices[2] + 1:]])
            
    #         break
    #     else:
    #         if password[indices[0]] not in string.punctuation:
    #             indices[0] = secrets.randbelow(len(password))
    #         elif password[indices[1]] not in string.punctuation:
    #             indices[1] = secrets.randbelow(len(password))
    #         elif password[indices[2]] not in string.punctuation:
    #             indices[2] = secrets.randbelow(len(password))

#########################################################################################################

csvinput['threeSubstitution'] = threeSubstitution
csvinput['threeSubstitution'] = csvinput['threeSubstitution'].apply(' '.join)

csvinput['threeInsertion'] = threeInsertion
csvinput['threeInsertion'] = csvinput['threeInsertion'].apply(' '.join)

csvinput['threeDeletion'] = threeDeletion
csvinput['threeDeletion'] = csvinput['threeDeletion'].apply(' '.join)

csvinput['threeCapMistake'] = threeCapMistake
csvinput['threeCapMistake'] = csvinput['threeCapMistake'].apply(' '.join)

# csvinput['subPunctuation'] = subPunctuation
# csvinput['subPunctuation'] = csvinput['subPunctuation'].apply(' '.join)

csvinput.to_csv("randomlyGeneratedPasswords.csv", index = False, quoting = csv.QUOTE_ALL)

