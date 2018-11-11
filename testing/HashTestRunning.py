import tlsh
import os

password = 'swordfish'
f = open('salt.txt' , 'r')
saltLines = f.read()
salt = saltLines.splitlines()
multiplier = 5

correctCombine = salt[0] + (password * multiplier) + salt[1]
hashOutput = tlsh.forcehash(correctCombine.encode("utf-8"))

triesRemaining = 10

beingAttackedFlag = False 

while True:
	incorrectPW = input('Password: ')
	incorrectCombine = salt[0] + (incorrectPW * multiplier) + salt[1]
	incorrectHashOutput = tlsh.forcehash(incorrectCombine.encode("utf-8"))
	diff = tlsh.diff(hashOutput , incorrectHashOutput)
	print ('Attempted password: ' + incorrectPW)
	print ('difference score: ' + str(diff))
	print ()