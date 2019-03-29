import os
from base64 import b64encode

saltArr = []
for i in range (2):
	saltArr.append((b64encode(os.urandom(16))).decode('utf-8'))

f = open('salt.txt' , 'w')
f.write("%s \n %s \n" % (saltArr[0], saltArr[1]))
f.close
