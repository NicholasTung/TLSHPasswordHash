import os

saltArr = []
for i in range (2):
	saltArr.append(str(os.urandom(16)))

f = open('salt.txt' , 'w')
f.write("%s \n %s \n" % (saltArr[0], saltArr[1]))
f.close
