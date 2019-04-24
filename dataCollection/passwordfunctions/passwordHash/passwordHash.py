import string
import secrets
import tlsh

def hash(password, prefixSalt, suffixSalt, multiplier):
	'''
	Correctly hash the provided passwords using the salts and multiplier
	'''
	return tlsh.forcehash((prefixSalt + (password * multiplier) + suffixSalt).encode("utf-8"))

def diff(passwordHash, otherHash):
	'''
	Uses TLSH difference function to return hash difference, for consistency I guess...
	'''
	return tlsh.diff(passwordHash, otherHash)
