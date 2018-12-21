import tlsh
import mysql.connector
import secrets
import os
import string
from base64 import b64encode

try:
    db = mysql.connector.connect(host = "localhost", user = secrets.username, password = secrets.password, database = "TLSHPasswordHash")
except:
    print ("Unable to connect to server")

cursor = db.cursor(prepared = True)

retry = True
multiplier = 5

def genSalts(newUser):
    print ("STARTED RUNNING GEN SALTS")
    print("about to create saltArr for" + newUser)
    saltArr = []
    print("created salt arr")
    for i in range (2):
        print ("about to append salts")
        saltArr.append((b64encode(os.urandom(19))).decode('utf-8'))
        print ("created salt #" + str(i))
        print()
        saltArr[i] = saltArr[i][:-3]
        print(saltArr[i])
        print()

    print ("filled salt arr")

    sql = "UPDATE userData SET prefixSalt = %s, suffixSalt = %s WHERE %s = user;"

    try:
        print ("executing salt update")
        cursor.execute(sql, (saltArr[0], saltArr[1], newUser))
        print ("executed salt insert")
    except:
        print ("Unable to execute")
        return None

    try:
        print ("commiting salts")
        db.commit()
        print ("committed salts")
    except:
        print("unable to commit")
        return None
def login():
    user = str(input("Username: "))

    sql = "SELECT * FROM userData WHERE %s = user;"

    try:
        cursor.execute(sql, (user,))
        results = cursor.fetchall()
        print(len(results))
        if len(results) > 0:
            for row in results:
                preSalt = row[1]
                sufSalt = row[2]
                passwordHash = row[3]
                remainingTries = row[4]
        else:
            print("Username does not exist")
            return None
    except:
        print ("Unable to fetch data")
        return None

    if remainingTries > 0:
        attemptedPass = str(input("Password: "))
        attemptedPassCombine = preSalt + (attemptedPass * multiplier) + sufSalt
        print(attemptedPassCombine)
        attemptedPassHash = tlsh.forcehash(attemptedPassCombine.encode('utf-8'))
        
        if passwordHash != attemptedPassHash:
            diff = tlsh.diff(passwordHash, attemptedPassHash)
            print(diff)
            if diff > 70 and diff < 130:
                cursor.execute("UPDATE userData SET remainingTries = remainingTries - 1 WHERE %s = user;", (user,))
                print ("Incorrect.")
            elif diff > 130 and remainingTries > 2:
                cursor.execute("UPDATE userData SET remainingTries = 2 WHERE %s = user;", (user,))
                print ("Incorrect.")
            elif diff > 130 and remainingTries <= 2:
                cursor.execute("UPDATE userData SET remainingTries = remainingTries - 1 WHERE %s = user;", (user,))
                print ("Incorrect.")
            else:
                print ("Incorrect")

            db.commit()
        elif passwordHash == attemptedPassHash:
            print ("You have successfully logged in.")
    elif remainingTries == 0:
        print ("This account is locked. Try again later.")
def register():
    newUser = str(input("Enter a username: "))

    sql = "SELECT * FROM userData WHERE %s = user"

    try:
        print ("Executing sql...")
        cursor.execute(sql, (newUser,))
        print ("successfully executed sql")
        print ("fetching...")
        results = cursor.fetchall()
        print ("fetched.")
        print (len(results))
        if len(results) != 0:
            print ("This username is taken. Try again.")
            return None
        elif len(results) == 0:
            print ("username is available")
            sql = "INSERT INTO userData (user) VALUES (%s);"

            try:
                print ("executing insert")
                cursor.execute(sql, (newUser,))
                print ("inserted")
            except:
                print ("Unable to make row")
            
            try:
                print ("committing")
                db.commit()
                print ("committed")
            except:
                print ("unable to commit")

            #genSalts(newUser)
    except:
        print ("Unable to fetch data nerrrrrrrrd")
        return None

    print ("Please enter a password that is at least 9 characters, and has 1 capital letter, 1 special character, and 1 number.")
    print ("This system does not penalize people that enter a password that is slightly incorrect, so consider using a more robust password.")
    print ("If you don't already have a robust password, try making a memorable sentence \n and use the first letter of each word of the sentence to generate your password.")

    retryPass = True

    while (retryPass):
        newUserPassword = str(input("Enter a password: "))

        invalidChars = set(string.punctuation)
        uppers = [l for l in newUserPassword if l.isupper()]

        if (len(newUserPassword) < 9):
            print ("Must be at least 9 characters long")
        elif not any(char in invalidChars for char in newUserPassword):
            print ("Must have at least 1 special character. Try again.")
        elif len(uppers) == 0:
            print ("Must have at least 1 capital letter. Try again.")
        elif not (any(char.isdigit() for char in newUserPassword)):
            print ("Must have at least 1 digit. Try again.")
        else:
            retryPass = False

    reEnterPass = True

    while (reEnterPass):
        reEnterPassword = str(input("Re-enter password: "))

        if newUserPassword != reEnterPassword:
            print ("These passwords do not match. Try again.")
        else:
            reEnterPass = False

    try:
        genSalts(newUser)
        print("generated salts")
    except NotImplementedError as ex:
        print(ex)

    sql = "SELECT prefixSalt, suffixSalt FROM userData WHERE %s = user;"

    try:
        cursor.execute(sql, (newUser,))
        newUserSaltsArr = cursor.fetchall()

        for row in newUserSaltsArr:
            newUserPreSalt = row[0]
            newUserSufSalt = row[1]
    except:
        print ("Unable to fetch salts")
        return None

    newUserPasswordCombine = newUserPreSalt + (newUserPassword * multiplier) + newUserSufSalt

    newUserPasswordHash = tlsh.forcehash(newUserPasswordCombine.encode("utf-8"))

    sql = "UPDATE userData SET passwordHash = %s, remainingTries = 10, accountLockFlag = 0 WHERE %s = user;"

    try:
        cursor.execute(sql, (newUserPasswordHash, newUser))
    except:
        print ("Unable to update table")
        return None

    db.commit()

while (retry):
    print ("Welcome to my scuffed program...")
    print ("Would you like to register an account of login to a pre-existing account?")
    print ("\t 1. Login \n \t 2. Register \n \t 3. Exit")

    choice = int(input("Enter a number: "))

    if choice == 1:
        login()
    elif choice == 2:
        register()
    elif choice == 3:
        exit()
