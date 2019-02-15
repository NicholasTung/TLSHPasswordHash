import string
import pandas as pd
import secrets
import tlsh
import csv

csvinput = pd.read_csv('randomlyGeneratedPasswords.csv')

oneInsertionDifference = list()
oneDeletionDiffernce = list()
oneSubstitutionDifference = list()

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

	print (tlsh.diff(controlHashed, passwordHashed))
	oneInsertionDifference.append([tlsh.diff(passwordHashed, insertionStrHashed)])
	oneDeletionDiffernce.append([tlsh.diff(passwordHashed, deletionStrHashed)])
	oneSubstitutionDifference.append([tlsh.diff(passwordHashed, substitutionStrHashed)])

csvinput['oneInsertionDifference'] = oneInsertionDifference
csvinput['oneInsertionDifference'] = csvinput['oneInsertionDifference'].str[0]

csvinput['oneDeletionDiffernce'] = oneDeletionDiffernce
csvinput['oneDeletionDiffernce'] = csvinput['oneDeletionDiffernce'].str[0]

csvinput['oneSubstitutionDifference'] = oneSubstitutionDifference
csvinput['oneSubstitutionDifference'] = csvinput['oneSubstitutionDifference'].str[0]

csvinput.to_csv("randomlyGeneratedPasswords.csv", index = False, quoting = csv.QUOTE_ALL)