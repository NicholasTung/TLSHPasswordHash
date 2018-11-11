import tlsh
import os

password = 'swordfish'
f = open('salt.txt' , 'r')
saltLines = f.read()
salt = saltLines.splitlines()
multiplier = 5

incorrectPWArray = ['swordfish', 
					'awordfish', 
					'aaordfish',
					'aaardfish', 
					'swordfisa', 
					'swordfiaa',
					'swordfaaa', 
					'aaaaaaaaa', 
					'zzzzzzzzz', 
					'swordfis', 
					'wordfish',
					'sordfish',
					'swordfisha',
					'aswordfish',
					'aaswordfish',
					'swordfishaa',
					'haufkljdioja',
					' ' ]
incorrectPWCharDifference = [0, 1, 2, 3, 1, 2, 3, 9, 9, 1, 1, 1, 1, 1, 2, 2, 12, 9]

correctCombine = salt[0] + (password * multiplier) + salt[1]
hashOutput = tlsh.forcehash(correctCombine.encode("utf-8"))

for i in range(len(incorrectPWArray)):
	incorrectCombine = salt[0] + (incorrectPWArray[i] * multiplier) + salt[1]
	incorrectHashOutput = tlsh.forcehash(incorrectCombine.encode("utf-8"))
	diff = tlsh.diff(hashOutput , incorrectHashOutput)
	print ('Attempted password: ' + incorrectPWArray[i])
	print ('Character Difference: ' + str(incorrectPWCharDifference[i]))
	print ('difference score: ' + str(diff))
	print ()




