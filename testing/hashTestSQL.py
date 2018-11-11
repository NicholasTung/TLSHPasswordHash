import tlsh
import MySQLdb
import secrets

db = MySQLdb.connect("localhost", secrets.username, secrets.password, "userData")
cursor = db.cursor()

retry = True

while (retry):
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

	if remainingTries > 0:
		attemptedPass = str(input("Password: "))
		attemptedPassCombine = preSalt + (attemptedPass * 5) + sufSalt
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
		elif passwordHash == attemptedPassHash:
			print ("Correct.")
	elif remainingTries < 0:
		print ("This account is locked. Try again later.")

	




		


