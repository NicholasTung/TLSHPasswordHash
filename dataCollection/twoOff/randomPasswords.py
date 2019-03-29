import string
import pandas as pd
import csv
import secrets
from base64 import b64encode
import os
import hashlib

s = hashlib.sha1()

specialChars = list(string.punctuation)
specialChars.remove(",")
specialChars.remove("'")
specialChars.remove('"')

randomCharset = string.ascii_lowercase + string.ascii_lowercase  + string.ascii_lowercase+ string.ascii_uppercase + string.digits + ''.join(specialChars)

def pw_generator(size=6, chars=randomCharset):
    result = ''.join(secrets.choice(chars) for _ in range(size))

    if not any(char in specialChars for char in result):
    	insert = secrets.randbelow(len(result))
    	result = result[:insert] + secrets.choice(specialChars) + result[insert:]

    if not any(char in string.digits for char in result):
    	insert = secrets.randbelow(len(result))
    	result = result[:insert] + secrets.choice(string.digits) + result[insert:]

    #print (result)
    return result

csvfile = pd.DataFrame()

passwords = list()
prefixSalt = list()
suffixSalt = list()
incorrect = list()

for i in range(100):
	pw = pw_generator(10)
    ic = pw_generator(10)
	passwords.append([pw])
	prefixSalt.append([(b64encode(os.urandom(19))).decode('utf-8')[:-3]])
	suffixSalt.append([(b64encode(os.urandom(19))).decode('utf-8')[:-3]])
	incorrect.append([ic])


csvfile['Password'] = passwords
csvfile['Password'] = csvfile['Password'].apply(' '.join)

csvfile['incorrect'] = incorrect
csvfile['incorrect'] = csvfile['incorrect'].apply(' '.join)

csvfile['prefixSalt'] = prefixSalt
csvfile['prefixSalt'] = csvfile['prefixSalt'].apply(' '.join)

csvfile['suffixSalt'] = suffixSalt
csvfile['suffixSalt'] = csvfile['suffixSalt'].apply(' '.join)

csvfile.to_csv('randomlyGeneratedPasswords.csv', index = False, quoting = csv.QUOTE_ALL)