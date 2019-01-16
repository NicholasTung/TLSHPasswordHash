import string
import pandas as pd
import secrets

csvinput = pd.read_csv('randomlyGeneratedPasswords.csv')

oneSubstitution = list()
oneInsertion = list()
oneDeletion = list()

specialChars = list(string.punctuation)
specialChars.remove(",")

allChars = string.ascii_uppercase + string.ascii_lowercase + string.digits + ''.join(specialChars)

for password in csvinput['Password  ']:

    insert = secrets.randbelow(len(password))
    oneInsertion.append(password[:insert] + secrets.choice(allChars) + password[insert:])

    delete = secrets.randbelow(len(password))
    oneDeletion.append(password[:delete] + password[(delete + 1):])

    insert = secrets.randbelow(len(password))
    oneSubstitution.append(password[:insert] + secrets.choice(allChars) + password[insert:])

csvinput['oneSubstitution  '] = oneSubstitution
csvinput['oneInsertion  '] = oneInsertion
csvinput['oneDeletion  '] = oneDeletion

csvinput.to_csv("randomlyGeneratedPasswords.csv", index = False)

