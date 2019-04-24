import string
import secrets
import charsets

allChars = charsets.allChars

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

def insertThree(password):
	indices = genThree(password)

    return password[indices[0]] + secrets.choice(allChars) + password[indices[0] + 1:indices[1]]
                         + secrets.choice(allChars) + password[indices[1]:indices[2]] 
                         + secrets.choice(allChars) + password[indices[2]:]

def substituteThree(password):
	indices = genThree(password)
    
    return password[:indices[0]] + secrets.choice(allChars) + password[indices[0] + 1:indices[1]]
                         + secrets.choice(allChars) + password[indices[1] + 1:indices[2]]
                         + secrets.choice(allChars) + password[indices[2] + 1:]

def deleteThree(password):
	indices = genThree(password)
    
    return password[:indices[0]] + password[indices[0] + 1:indices[1]]
                         + password[indices[1] + 1:indices[2]] + password[indices[2] + 1:]

def capitalizeThree(password):
	indices = genThree(password)
    
    while True:
        if password[indices[0]] in string.ascii_letters and password[indices[1]] in string.ascii_letters and password[indices[2]] in string.ascii_letters:
            return password[:indices[0]] + toggleCapitalization(password[indices[0]]) + password[indices[0] + 1:indices[1]]
                         + toggleCapitalization(password[indices[1]]) + password[indices[1] + 1:indices[2]]
                         + toggleCapitalization(password[indices[2]]) + password[indices[2] + 1:]
            
            break
        else:
            if password[indices[0]] not in string.ascii_letters:
                indices[0] = secrets.randbelow(len(password))
            elif password[indices[1]] not in string.ascii_letters:
                indices[1] = secrets.randbelow(len(password))
            elif password[indices[2]] not in string.ascii_letters:
                indices[2] = secrets.randbelow(len(password))