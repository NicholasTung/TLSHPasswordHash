import string

specialChars = list(string.punctuation)
specialChars.remove(",")

allChars = string.ascii_uppercase + string.ascii_lowercase + string.digits + ''.join(specialChars)