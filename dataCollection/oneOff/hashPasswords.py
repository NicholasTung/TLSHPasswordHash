import string
import pandas as pd
import secrets
import tlsh
import csv

csvinput = pd.read_csv('randomlyGeneratedPasswords.csv')

oneInsertionDifference = list()
oneDeletionDiffernce = list()
oneSubstitutionDifference = list()
incorrectDifference = list()
oneCapDifference = list()
# subPuncDifference = list()

multiplier = 5

for password in csvinput["Password"]:
	password = csvinput.loc[csvinput["Password"] == password, 'Password'].values[0]
	prefixSalt = csvinput.loc[csvinput["Password"] == password, 'prefixSalt'].values[0]
	suffixSalt = csvinput.loc[csvinput["Password"] == password, 'suffixSalt'].values[0]

	passwordHashed = tlsh.forcehash((prefixSalt + (password * multiplier) + suffixSalt).encode("utf-8"))
	controlHashed = tlsh.forcehash((prefixSalt + ("PASSWORD" * multiplier) + suffixSalt).encode("utf-8"))

	insertionStr = csvinput.loc[csvinput["Password"] == password, 'oneInsertion'].values[0]
	insertionStrHashed = tlsh.forcehash((prefixSalt + (insertionStr * multiplier) + suffixSalt).encode("utf-8"))

	deletionStr = csvinput.loc[csvinput["Password"] == password, 'oneDeletion'].values[0]
	deletionStrHashed = tlsh.forcehash((prefixSalt + (deletionStr * multiplier) + suffixSalt).encode("utf-8"))

	substitutionStr = csvinput.loc[csvinput["Password"] == password, 'oneSubstitution'].values[0]
	substitutionStrHashed = tlsh.forcehash((prefixSalt + (substitutionStr * multiplier) + suffixSalt).encode("utf-8"))

	incorrectStr = csvinput.loc[csvinput["Password"] == password, 'incorrect'].values[0]
	incorrectStrHashed = tlsh.forcehash((prefixSalt + (incorrectStr * multiplier) + suffixSalt).encode("utf-8"))

	capStr = csvinput.loc[csvinput["Password"] == password, 'oneCapMistake'].values[0]
	capStrHashed = tlsh.forcehash((prefixSalt + (capStr * multiplier) + suffixSalt).encode("utf-8"))

	# subPuncStr = csvinput.loc[csvinput["Password"] == password, 'subPunctuation'].values[0]
	# subPuncHashed = tlsh.forcehash((prefixSalt + (subPuncStr * multiplier) + suffixSalt).encode("utf-8"))

	oneInsertionDifference.append(tlsh.diff(passwordHashed, insertionStrHashed))
	oneDeletionDiffernce.append(tlsh.diff(passwordHashed, deletionStrHashed))
	oneSubstitutionDifference.append(tlsh.diff(passwordHashed, substitutionStrHashed))
	incorrectDifference.append(tlsh.diff(passwordHashed, incorrectStrHashed))
	oneCapDifference.append(tlsh.diff(passwordHashed, capStrHashed))
	# subPuncDifference.append(tlsh.diff(passwordHashed, subPuncHashed))

csvinput['oneSubstitutionDifference'] = pd.Series(oneSubstitutionDifference, dtype = int)
#csvinput['oneSubstitutionDifference'] = csvinput['oneSubstitutionDifference'].str[0]
#csvinput['oneSubstitutionDifference'] = csvinput['oneSubstitutionDifference'].astype(object)

csvinput['oneInsertionDifference'] = pd.Series(oneInsertionDifference, dtype = int)
#csvinput['oneInsertionDifference'] = csvinput['oneInsertionDifference'].str[0]
#csvinput['oneInsertionDifference'] = csvinput['oneInsertionDifference'].astype(object)

csvinput['oneDeletionDiffernce'] = pd.Series(oneDeletionDiffernce, dtype = int)
#csvinput['oneDeletionDiffernce'] = csvinput['oneDeletionDiffernce'].str[0]
#csvinput['oneDeletionDiffernce'] = csvinput['oneDeletionDiffernce'].astype(object)

csvinput['oneCapDifference'] = pd.Series(oneCapDifference, dtype = int)

# csvinput['subPuncDifference'] = pd.Series(subPuncDifference, dtype = int)

csvinput['incorrectDifference'] = pd.Series(incorrectDifference, dtype = int)
#csvinput['incorrectDifference'] = csvinput["incorrectDifference"].str[0]
#csvinput['incorrectDifference'] = csvinput["incorrectDifference"].astype(object)

csvinput.to_csv("randomlyGeneratedPasswords.csv", index = False, quoting = csv.QUOTE_NONNUMERIC)