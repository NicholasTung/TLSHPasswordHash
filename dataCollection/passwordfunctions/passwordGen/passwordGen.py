import string
import secrets
from base64 import b64encode
import os

specialChars = list(string.punctuation)
specialChars.remove(",")
specialChars.remove("'")
specialChars.remove('"')

randomCharset = string.ascii_lowercase + string.ascii_lowercase  + string.ascii_lowercase+ string.ascii_uppercase + string.digits + ''.join(specialChars)

def genPassword(size=10, chars=randomCharset):
    '''
    Generates a random password guaranteed to have a special charcater and digit
    
    The default charcaterset is a concatenation of some python charactersets,
    made to increase the likelihood of certian characters being chosen
    '''
    result = ''.join(secrets.choice(chars) for _ in range(size))
    if not any(char in specialChars for char in result):
        insert = secrets.randbelow(len(result))
        result = result[:insert] + secrets.choice(specialChars) + result[insert:]

    if not any(char in string.digits for char in result):
        insert = secrets.randbelow(len(result))
        result = result[:insert] + secrets.choice(string.digits) + result[insert:]

    return result

def genSalts():
    '''
    Generates a random salt
    '''
    salt = (b64encode(os.urandom(19))).decode('utf-8')[:-3]
    return salt