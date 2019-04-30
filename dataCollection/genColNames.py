'''
Quickly generate column names with the appropriate suffix
'''
addition = "Mean"
names = ["oneInsert", "oneDelete", "oneSubstitute", "oneCapitalize", 
	    "twoInsert", "twoDelete", "twoSubstitute", "twoCapitalize, 
	    "threeInsert", "threeDelete", "threeSubstitute", "threeCapitalize"]

for name in names:
	print(name + addition, end = ", ")