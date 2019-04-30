'''
Generates dataframes for raw string data, hashed data, and difference scores
Stores them using pickle
'''
from passwordfunctions.passwordGen import passwordGen as pg
from passwordfunctions.passwordVary import varyOne as pv1
from passwordfunctions.passwordVary import varyTwo as pv2
from passwordfunctions.passwordVary import varyThree as pv3
from passwordfunctions.passwordHash import passwordHash as ph

import pandas
import pickle
import re

#Functions
def pwsGenerator(function, numIter):
    for i in range(numIter):
        yield function()

def varyGenerator(function, pwSeries):
    for pw in pwSeries.iteritems():
        yield function(pw[1])

def hashGenerator(name, df, multiplier):
    for pw, prefixSalt, suffixSalt in zip(df[name].iteritems(), df["prefixSalt"].iteritems(), df["suffixSalt"].iteritems()):
        yield ph.hash(pw[1], prefixSalt[1], suffixSalt[1], multiplier)

def diffGenerator(oHashSeries, wHashSeries):
    for opw, wpw in zip(oHashSeries.iteritems(), wHashSeries.iteritems()):
        yield ph.diff(opw[1], wpw[1])

def makeVarySeries(name, function, df):
    return pandas.Series(list(varyGenerator(function, df[name])))

def makeDiffSeries(name, df):
    return pandas.Series(diffGenerator(df["password"], df[name[:-10]]))

def makeHashedSeries(name, df, multiplier):
    return pandas.Series(hashGenerator(name, df, multiplier))

iterations = 10000
multiplier = 5

passwordsColumns = ["password", "prefixSalt", "suffixSalt", 
                    "oneInsert", "oneDelete", "oneSubstitute", "oneCapitalize", 
                    "twoInsert", "twoDelete", "twoSubstitute", "twoCapitalize", 
                    "threeInsert", "threeDelete", "threeSubstitute", "threeCapitalize"]
passwords = pandas.DataFrame(columns = passwordsColumns)

for baseCol in passwordsColumns[0:3]:
    if baseCol is passwordsColumns[0]:
        passwords[baseCol] = pandas.Series(pwsGenerator(pg.genPassword, iterations))
    elif baseCol in passwordsColumns[1:3]:
        passwords[baseCol] = pandas.Series(pwsGenerator(pg.genSalts, iterations))

for varyCol1 in passwordsColumns[3:7]:
    splitName1 = re.findall(".+?(?:(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])|$)", varyCol1)
    fvaryCol1 = splitName1[1].lower() + splitName1[0].capitalize()
    passwords[varyCol1] = makeVarySeries("password", getattr(pv1, fvaryCol1), passwords)

for varyCol2 in passwordsColumns[7:11]:
    splitName2 = re.findall(".+?(?:(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])|$)", varyCol2)
    fvaryCol2 = splitName2[1].lower() + splitName2[0].capitalize()
    passwords[varyCol2] = makeVarySeries("password", getattr(pv2, fvaryCol2), passwords)

for varyCol3 in passwordsColumns[11:15]:
    splitName3 = re.findall(".+?(?:(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])|$)", varyCol3)
    fvaryCol3 = splitName3[1].lower() + splitName3[0].capitalize()
    passwords[varyCol3] = makeVarySeries("password", getattr(pv3, fvaryCol3), passwords)

hashedColumns = ["password",
                 "oneInsert", "oneDelete", "oneSubstitute", "oneCapitalize", 
                 "twoInsert", "twoDelete", "twoSubstitute", "twoCapitalize", 
                 "threeInsert", "threeDelete", "threeSubstitute", "threeCapitalize"]
hashed = pandas.DataFrame(columns = hashedColumns)

for hashCol in hashedColumns:
    hashed[hashCol] = makeHashedSeries(hashCol, passwords, multiplier)

dataColumns = ["oneInsertDifference", "oneDeleteDifference", "oneSubstituteDifference", "oneCapitalizeDifference", 
               "twoInsertDifference", "twoDeleteDifference", "twoSubstituteDifference", "twoCapitalizeDifference", 
               "threeInsertDifference", "threeDeleteDifference", "threeSubstituteDifference", "threeCapitalizeDifference"]
data = pandas.DataFrame(columns = dataColumns, dtype=float)

for dataCol in dataColumns:
    data[dataCol] = makeDiffSeries(dataCol, hashed)

print(passwords)
print(hashed)
print(data)

passwords.to_pickle("~/git/TLSHPasswordHash/dataCollection/dataframePickles/passwords.pkl")
hashed.to_pickle("~/git/TLSHPasswordHash/dataCollection/dataframePickles/hashed.pkl")
passwords.to_pickle("~/git/TLSHPasswordHash/dataCollection/dataframePickles/data.pkl")



