from passwordfunctions.passwordGen import passwordGen as pg
from passwordfunctions.passwordVary import * as pv
from passwordfunctions.passwordHash import passwordHash as ph
import pandas
import pickle

iterations = 10000

passwordsColumns = ["password", "prefixSalt", "suffixSalt", 
			  "oneInsert", "oneDelete", "oneSubstitute", "oneCapitalize", 
			  "twoInsert", "twoDelete", "twoSubstitute", "twoCapitalize, 
			  "threeInsert", "threeDelete", "threeSubstitute", "threeCapitalize"]
passwords = pandas.DataFrame(passwordsColumns)

for baseCol in passwordsColumns[0:3]:
	if baseCol is passwordsColumns[0]:
		passwords[baseCol] = pandas.Series(pwsGenerator(pg.genPassword, iterations))
	elif baseCol in passwordsColumns[1:3]:
		passwords[baseCol] = pandas.Series(pwsGenerator(pg.genSalts, iterations))

for varyCol in passwordsColumns[3:15]:
	passwords[varyCol] = makeVarySeries(varyCol, iterations, passwords)

dataColumns = ["zeroes", "two-fifties"
			   "oneInsertDifference", "oneDeleteDifference", "oneSubstituteDifference", "oneCapitalizeDifference", 
			   "twoInsertDifference", "twoDeleteDifference", "twoSubstituteDifference", "twoCapitalizeDifference", 
			   "threeInsertDifference", "threeDeleteDifference", "threeSubstituteDifference", "threeCapitalizeDifference",
			   "oneMean", "twoMean", "threeMean", 
			   "overallMean", "overallSTDEV", "upperBound", "lowerBound", "boundSize"]

data = pandas.DataFrame(dataColumns)

graphsColumns = ["apc12Ins", "apc12Del", "apc12Sub", "apc12Cap"
				 "apc23Ins", "apc23Del", "apc23Sub", "apc23Cap"]

def pwsGenerator(function, numIter):
	for i in range(numiter):
		yield function()

def varyGenerator(function, numIter, pwSeries):
	for pw in pwSeries.iteritems():
		yield function(pw)

def makeVarySeries(name, numIter, df):
	return pandas.Series(pwsGenerator(getattr(pv, name), numIter, df[name]))