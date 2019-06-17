import string
import pandas as pd
import secrets
import tlsh
import csv

csvinput = pd.read_csv('randomlyGeneratedPasswords.csv')

twoInsertionDifference = list()
twoDeletionDiffernce = list()
twoSubstitutionDifference = list()
incorrectDifference = list()
twoCapDifference = list()
# subPuncDifference = list()

multiplier = 5

for password in csvinput["Password"]:
	password = csvinput.loc[csvinput["Password"] == password, 'Password'].values[0]
	prefixSalt = csvinput.loc[csvinput["Password"] == password, 'prefixSalt'].values[0]
	suffixSalt = csvinput.loc[csvinput["Password"] == password, 'suffixSalt'].values[0]

	passwordHashed = tlsh.forcehash((prefixSalt + (password * multiplier) + suffixSalt).encode("utf-8"))
	controlHashed = tlsh.forcehash((prefixSalt + ("PASSWORD" * multiplier) + suffixSalt).encode("utf-8"))

	insertionStr = csvinput.loc[csvinput["Password"] == password, 'twoInsertion'].values[0]
	insertionStrHashed = tlsh.forcehash((prefixSalt + (insertionStr * multiplier) + suffixSalt).encode("utf-8"))

	deletionStr = csvinput.loc[csvinput["Password"] == password, 'twoDeletion'].values[0]
	deletionStrHashed = tlsh.forcehash((prefixSalt + (deletionStr * multiplier) + suffixSalt).encode("utf-8"))

	substitutionStr = csvinput.loc[csvinput["Password"] == password, 'twoSubstitution'].values[0]
	substitutionStrHashed = tlsh.forcehash((prefixSalt + (substitutionStr * multiplier) + suffixSalt).encode("utf-8"))

	incorrectStr = csvinput.loc[csvinput["Password"] == password, 'incorrect'].values[0]
	incorrectStrHashed = tlsh.forcehash((prefixSalt + (incorrectStr * multiplier) + suffixSalt).encode("utf-8"))

	capStr = csvinput.loc[csvinput["Password"] == password, 'twoCapMistake'].values[0]
	capStrHashed = tlsh.forcehash((prefixSalt + (capStr * multiplier) + suffixSalt).encode("utf-8"))

	# subPuncStr = csvinput.loc[csvinput["Password"] == password, 'subPunctuation'].values[0]
	# subPuncHashed = tlsh.forcehash((prefixSalt + (subPuncStr * multiplier) + suffixSalt).encode("utf-8"))

	twoInsertionDifference.append(tlsh.diff(passwordHashed, insertionStrHashed))
	twoDeletionDiffernce.append(tlsh.diff(passwordHashed, deletionStrHashed))
	twoSubstitutionDifference.append(tlsh.diff(passwordHashed, substitutionStrHashed))
	incorrectDifference.append(tlsh.diff(passwordHashed, incorrectStrHashed))
	twoCapDifference.append(tlsh.diff(passwordHashed, capStrHashed))
	# subPuncDifference.append(tlsh.diff(passwordHashed, subPuncHashed))

csvinput['twoSubstitutionDifference'] = pd.Series(twoSubstitutionDifference, dtype = int)
#csvinput['twoSubstitutionDifference'] = csvinput['twoSubstitutionDifference'].str[0]
#csvinput['twoSubstitutionDifference'] = csvinput['twoSubstitutionDifference'].astype(object)

csvinput['twoInsertionDifference'] = pd.Series(twoInsertionDifference, dtype = int)
#csvinput['twoInsertionDifference'] = csvinput['twoInsertionDifference'].str[0]
#csvinput['twoInsertionDifference'] = csvinput['twoInsertionDifference'].astype(object)

csvinput['twoDeletionDiffernce'] = pd.Series(twoDeletionDiffernce, dtype = int)
#csvinput['twoDeletionDiffernce'] = csvinput['twoDeletionDiffernce'].str[0]
#csvinput['twoDeletionDiffernce'] = csvinput['twoDeletionDiffernce'].astype(object)

csvinput['twoCapDifference'] = pd.Series(twoCapDifference, dtype = int)

# csvinput['subPuncDifference'] = pd.Series(subPuncDifference, dtype = int)

csvinput['incorrectDifference'] = pd.Series(incorrectDifference, dtype = int)
#csvinput['incorrectDifference'] = csvinput["incorrectDifference"].str[0]
#csvinput['incorrectDifference'] = csvinput["incorrectDifference"].astype(object)

csvinput.to_csv("randomlyGeneratedPasswords.csv", index = False, quoting = csv.QUOTE_NONNUMERIC)