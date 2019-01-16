import string
import csv
import secrets

specialChars = list(string.punctuation)
specialChars.remove(",")

def pw_generator(size=6, chars=string.ascii_uppercase + string.ascii_lowercase + string.digits + ''.join(specialChars)):
    result = ''.join(secrets.choice(chars) for _ in range(size))

    if not any(char in specialChars for char in result):
    	insert = secrets.randbelow(len(result))
    	result = result[:insert] + secrets.choice(specialChars) + result[insert:]

    if not any(char in string.digits for char in result):
    	insert = secrets.randbelow(len(result))
    	result = result[:insert] + secrets.choice(string.digits) + result[insert:]

    #print (result)
    return result

csvfile = open('randomlyGeneratedPasswords.csv', 'w')

writer = csv.writer(csvfile, delimiter = ",", quoting = csv.QUOTE_ALL)

writer.writerow(["Password  "])

for i in range(0, 100):
	writer.writerow([pw_generator(10)])
