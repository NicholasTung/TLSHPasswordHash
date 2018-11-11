import tlsh
import MySQLdb
import secrets
import os
import string

db = MySQLdb.connect("localhost", secrets.username, secrets.password, "userData")
cursor = db.cursor()

retry = True
multiplier = 5

while (retry):
	# for later

def login():
	user = str(input("Username: "))

	sql = "SELECT * FROM userData WHERE user = %s;" % user

	try:
		cursor.execute(sql)
		results = cursor.fetchall()
		for row in results:
			user = row[0]
			preSalt = row[1]
			sufSalt = row[2]
			passwordHash = row[3]
			remainingTries = row[4]
	except:
		print ("Unable to fetch data")
		return None

	if remainingTries > 0:
		attemptedPass = str(input("Password: "))
		attemptedPassCombine = preSalt + (attemptedPass * multiplier) + sufSalt
		attemptedPassHash = tlsh.forcehash(attemptedPassCombine.encode("utf-8"))
		
		if passwordHash != attemptedPassHash:
			diff = tlsh.diff(passwordHash, attemptedPassHash)
			if diff > 100 && diff < 200:
				cursor.execute("UPDATE userData SET remainingTries = remainingTries - 1 WHERE user = %s;" % user)
				print ("Incorrect.")
			elif diff > 200 and remainingTries > 2:
				cursor.execute("UPDATE userData SET remainingTries = 2 WHERE user = %s;" % user)
				print ("Incorrect.")
			elif diff > 200 and remainingTries <= 2:
				cursor.execute("UPDATE userData SET remainingTries = remainingTries - 1 WHERE user = %s;" % user)
				print ("Incorrect.")
			else:
				print ("Incorrect")

			db.commit()
		elif passwordHash == attemptedPassHash:
			print ("You have successfully logged in.")
	elif remainingTries < 0:
		print ("This account is locked. Try again later.")
def register():
	newUser = str(input("Enter a username: "))

	sql = "SELECT * FROM userData WHERE user = %s;" % newUser

	try:
		cursor.execute(sql)
		results = cursor.fetchall()
		if len(results) != 0:
			print ("This username is taken. Try again.")
			return None
		elif len(results == 0):
			sql = "INSERT INTO userData (user) VALUES (%s);" % newUser

			try:
				cursor.execute(sql)
			except:
				print ("Unable to make row")
			genSalts(user)

			db.commit()
	except:
		print ("Unable to fetch data")

	print ("Please enter a password that is at least 9 characters, and has 1 capital letter, 1 special character, and 1 number.")
	print ("This system does not penalize people that enter a password that is slightly incorrect, so consider using a more robust password.")
	print ("If you don't already have a robust password, try making a memorable sentence \n and use the first letter of each word of the sentence to generate your password.")

	retryPass = True

	while (retryPass):
		newUserPassword = str(input("Enter a password: "))

		invalidChars = set(string.punctuation)
		uppers = [l for l in password if l.isupper()]

		if any(char in invalidChars for char in password):
    		print ("Must have at least 1 special character. Try again.")
    	elif len(uppers) == 0:
    		print ("Must have at least 1 capital letter. Try again.")
    	elif !(any(char.isdigit() for char in password)):
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

    sql = "SELECT prefixSalt, suffixSalt FROM userData WHERE user = %s;" % newUser

    try:
    	cursor.execute(sql)
    	newUserSaltsArr = cursor.fetchall()

    	for row in newUserSaltsArr:
    		newUserPreSalt = row[0]
    		newUserSufSalt = row[1]
    except:
    	print ("Unable to fetch salts")

    newUserPasswordCombine = newUserPreSalt + (newUserPassword * multiplier) + newUserSufSalt

    newUserPasswordHash = tlsh.forcehash(newUserPasswordCombine.encode("utf-8"))

    sql = "UPDATE userData SET passwordHash = %s, remainingTries = 10, accountLockFlag = 0 WHERE user = %s;" % (newUserPasswordHash, newUser)

    try:
    	cursor.execute(sql)
    except:
    	print ("Unable to update table")

    db.commit()

def genSalts(user):
	saltArr = []
	for i in range (2):
		saltArr.append(str(os.urandom(16)))
	
	sql = "UPDATE userData SET prefixSalt = %s, suffixSalt = %s WHERE user = %s" % (saltArr[0], saltArr[1], user)

	try:
		cursor.execute(sql)
	except:
		print ("Unable to update table")
		
	db.commit()


