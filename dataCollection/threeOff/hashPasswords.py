import string
import pandas as pd
import secrets
import tlsh
import csv

csvinput = pd.read_csv('randomlyGeneratedPasswords.csv')

threeInsertionDifference = list()
threeDeletionDiffernce = list()
threeSubstitutionDifference = list()
incorrectDifference = list()
threeCapDifference = list()
# subPuncDifference = list()

multiplier = 5

for password in csvinput["Password"]:
	password = csvinput.loc[csvinput["Password"] == password, 'Password'].values[0]
	prefixSalt = csvinput.loc[csvinput["Password"] == password, 'prefixSalt'].values[0]
	suffixSalt = csvinput.loc[csvinput["Password"] == password, 'suffixSalt'].values[0]

	passwordHashed = tlsh.forcehash((prefixSalt + (password * multiplier) + suffixSalt).encode("utf-8"))
	controlHashed = tlsh.forcehash((prefixSalt + ("PASSWORD" * multiplier) + suffixSalt).encode("utf-8"))

	insertionStr = csvinput.loc[csvinput["Password"] == password, 'threeInsertion'].values[0]
	insertionStrHashed = tlsh.forcehash((prefixSalt + (insertionStr * multiplier) + suffixSalt).encode("utf-8"))

	deletionStr = csvinput.loc[csvinput["Password"] == password, 'threeDeletion'].values[0]
	deletionStrHashed = tlsh.forcehash((prefixSalt + (deletionStr * multiplier) + suffixSalt).encode("utf-8"))

	substitutionStr = csvinput.loc[csvinput["Password"] == password, 'threeSubstitution'].values[0]
	substitutionStrHashed = tlsh.forcehash((prefixSalt + (substitutionStr * multiplier) + suffixSalt).encode("utf-8"))

	incorrectStr = csvinput.loc[csvinput["Password"] == password, 'incorrect'].values[0]
	incorrectStrHashed = tlsh.forcehash((prefixSalt + (incorrectStr * multiplier) + suffixSalt).encode("utf-8"))

	capStr = csvinput.loc[csvinput["Password"] == password, 'threeCapMistake'].values[0]
	capStrHashed = tlsh.forcehash((prefixSalt + (capStr * multiplier) + suffixSalt).encode("utf-8"))

	# subPuncStr = csvinput.loc[csvinput["Password"] == password, 'subPunctuation'].values[0]
	# subPuncHashed = tlsh.forcehash((prefixSalt + (subPuncStr * multiplier) + suffixSalt).encode("utf-8"))

	threeInsertionDifference.append(tlsh.diff(passwordHashed, insertionStrHashed))
	threeDeletionDiffernce.append(tlsh.diff(passwordHashed, deletionStrHashed))
	threeSubstitutionDifference.append(tlsh.diff(passwordHashed, substitutionStrHashed))
	incorrectDifference.append(tlsh.diff(passwordHashed, incorrectStrHashed))
	threeCapDifference.append(tlsh.diff(passwordHashed, capStrHashed))
	# subPuncDifference.append(tlsh.diff(passwordHashed, subPuncHashed))

csvinput['threeSubstitutionDifference'] = pd.Series(threeSubstitutionDifference, dtype = int)
#csvinput['threeSubstitutionDifference'] = csvinput['threeSubstitutionDifference'].str[0]
#csvinput['threeSubstitutionDifference'] = csvinput['threeSubstitutionDifference'].astype(object)

csvinput['threeInsertionDifference'] = pd.Series(threeInsertionDifference, dtype = int)
#csvinput['threeInsertionDifference'] = csvinput['threeInsertionDifference'].str[0]
#csvinput['threeInsertionDifference'] = csvinput['threeInsertionDifference'].astype(object)

csvinput['threeDeletionDiffernce'] = pd.Series(threeDeletionDiffernce, dtype = int)
#csvinput['threeDeletionDiffernce'] = csvinput['threeDeletionDiffernce'].str[0]
#csvinput['threeDeletionDiffernce'] = csvinput['threeDeletionDiffernce'].astype(object)

csvinput['threeCapDifference'] = pd.Series(threeCapDifference, dtype = int)

#csvinput['subPuncDifference'] = pd.Series(subPuncDifference, dtype = int)

csvinput['incorrectDifference'] = pd.Series(incorrectDifference, dtype = int)
#csvinput['incorrectDifference'] = csvinput["incorrectDifference"].str[0]
#csvinput['incorrectDifference'] = csvinput["incorrectDifference"].astype(object)

csvinput.to_csv("randomlyGeneratedPasswords.csv", index = False, quoting = csv.QUOTE_NONNUMERIC)