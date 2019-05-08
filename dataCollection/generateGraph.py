import matplotlib.pyplot as plt
import pandas as pd
import pickle
import numpy as np

prefix = ("one", "two", "three")
suffix = ("SubstituteDifference", "InsertDifference", "DeleteDifference", "CapitalizeDifference")

def genProgression(df):
    oneError, oneSEM = list(), list()
    twoError, twoSEM = list(), list()
    threeError, threeSEM = list(), list()
    incorrectError, incorrectSEM = list(), list()

    for s in suffix:
        oneError.append(df["one" + s].mean())
        oneSEM.append(df["one" + s].sem())

        twoError.append(df["two" + s].mean())
        twoSEM.append(df["two" + s].sem())

        threeError.append(df["three" + s].mean())
        threeSEM.append(df["three" + s].sem())

    for i in range(4):
        print(oneError[i])
        print(oneSEM[i])
        print()

    incorrectError = [df["incorrectDifference"].mean()] * 4
    incorrectSEM = [df["incorrectDifference"].sem()] * 4

    fig, ax = plt.subplots()
    index = np.arange(len(oneError))
    barWidth = .2

    alignment = 'edge'

    oneBars = ax.bar(index - barWidth, oneError, barWidth, align = alignment, color = 'b', label = 'One Error', yerr = oneSEM)
    twoBars = ax.bar(index, twoError, barWidth, align = alignment, color = 'r', label = 'Two Errors', yerr = twoSEM)
    threeBars = ax.bar(index + barWidth, threeError, barWidth, align = alignment, color = 'y', label = "Three Errors", yerr = threeSEM)
    incorrectBars = ax.bar(index + barWidth*2, incorrectError, barWidth, align = alignment, color = 'g', label = "Incorrect", yerr = incorrectSEM)

    ax.set_xlabel('Error Type')
    ax.set_ylabel("Score")
    ax.set_title("Progression of Scores with increasing errors")
    ax.set_xticks(index + barWidth)
    ax.set_xticklabels(("Substituiton", "Insertion", "Deletion", "Capitalization"))

    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])

    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    
    plt.show()


def genPercentProgression(df):
    calcDF = pd.DataFrame(dtype = np.float)

    resultNames = ["sub12", "ins12", "del12", "cap12", "sub23", "ins23", "del23", "cap23"]

    data12 = []
    data12SEM = []

    data23 = []
    data23SEM = []

    i = 0

    for s in resultNames:
        if s[-2:] == "12":
            suf = suffix[i]
            calcDF[s] = df["two" + suf].subtract(df["one" + suf]).divide(df["one" + suf])
        else:
            suf = suffix[i]
            calcDF[s] = ((df["three" + suf] - df["two" + suf]) / df["two" + suf])

        i += 1
        i = i % 4

    for s in resultNames:
        if s[-2:] == "12":
            data12.append(calcDF[s].mean())
            data12SEM.append(calcDF[s].sem())
        else:
            data23.append(calcDF[s].mean())
            data23SEM.append(calcDF[s].sem())

        i += 1
        i = i % 4

    fig, ax = plt.subplots()
    index = np.arange(len(data12))
    barWidth = .2
    alignment = 'edge'

    apc12Label = '1 error to 2 error passwords'
    apc23Label = '2 error to 3 error passwords'

    apc12Bar = ax.bar(index, data12, barWidth, align = alignment, color = 'b', label = apc12Label, yerr = data12SEM)
    apc23Bar = ax.bar(index + barWidth, data23, barWidth, align = alignment, color = 'r', label = apc23Label, yerr = data23SEM)

    ax.set_xlabel('Variations')
    ax.set_ylabel("Percentage")
    ax.set_title("Percent increase between passwords with different number of errors")
    ax.set_xticks(index + barWidth)
    ax.set_xticklabels(("Substituiton", "Insertion", "Deletion", "Capitalization"))

    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])

    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    
    plt.show()

def genVisualizer(df):
    calcDF = pd.DataFrame(dtype = np.float64)

    for p in prefix:
        cols = [p + suffix[0], p + suffix[1], p + suffix[2], p + suffix[3]]
        calcDF[p + "Avg"] = df[cols].mean(axis = 1)

    calcDF["average"] = calcDF[["oneAvg", "twoAvg", "threeAvg"]].mean(axis = 1)
    calcDF["stdev"] = calcDF["average"].std()
    calcDF["upper"] = calcDF["average"] + calcDF["stdev"]
    calcDF["lower"] = calcDF["average"] - calcDF["stdev"]

    lowerL = [calcDF["lower"].mean(), calcDF["lower"].sem()]
    upperL = [calcDF["upper"].mean() - lowerL[0], calcDF["upper"].sem()]

    fig, ax = plt.subplots()
    index = np.arange(len(upperL))
    barWidth = .2
    alignment = 'center'

    lowerBar = ax.bar(1, lowerL[0], barWidth, color = 'b', label = "No deduction", yerr = lowerL[1])
    upperBar = ax.bar(1, upperL[0], barWidth, bottom = lowerL[0], color = 'r', label = "Deduct one", yerr = upperL[1])
    topBar = ax.bar(1, 300 - lowerL[0] - upperL[0], barWidth, bottom = upperL[0] + lowerL[0], color = 'g', label = 'Lower to two')

    ax.set_ylabel("Score")
    ax.set_title("Visualization of Score Range Use")
    ax.set_xticklabels([])

    ax.legend(fancybox=True, shadow=True)

    plt.show()

def genStock(df):
    calcDF = pd.DataFrame(dtype = np.float64)

    for p in prefix:
        cols = [p + suffix[0], p + suffix[1], p + suffix[2], p + suffix[3]]
        calcDF[p + "Avg"] = df[cols].mean(axis = 1)

    calcDF["average"] = calcDF[["oneAvg", "twoAvg", "threeAvg"]].mean(axis = 1)
    calcDF["stdev"] = calcDF["average"].std()
    calcDF["upper"] = calcDF["average"] + calcDF["stdev"]
    calcDF["lower"] = calcDF["average"] - calcDF["stdev"]

    fig, ax = plt.subplots()
    index = np.arange(calcDF["upper"].size)
    barWidth = .02
    alignment = 'center'

    stockBar = ax.bar(index, calcDF["upper"].tolist(), barWidth, bottom = calcDF["lower"].tolist(), color = 'b', label = 'Deduct One Range')

    ax.set_xlabel('Password Number')
    ax.set_ylabel("Score")
    ax.set_title("Password Score Ranges")
    ax.set_xticks(index + barWidth)
    ax.set_xticklabels(index)

    ax.legend(fancybox = True, shadow = True)

    plt.show()

def genHistogram(df):
    calcDF = pd.DataFrame(dtype = np.float64)

    for p in prefix:
        cols = [p + suffix[0], p + suffix[1], p + suffix[2], p + suffix[3]]
        calcDF[p + "Avg"] = df[cols].mean(axis = 1)

    calcDF["average"] = calcDF[["oneAvg", "twoAvg", "threeAvg"]].mean(axis = 1)
    calcDF["stdev"] = calcDF["average"].std()
    calcDF["upper"] = calcDF["average"] + calcDF["stdev"]
    calcDF["lower"] = calcDF["average"] - calcDF["stdev"]
    calcDF["size"] = calcDF["upper"] - calcDF["lower"]

    print(calcDF["size"].mean())

    fig, ax = plt.subplots()
    barWidth = .2

    calcDF.hist(column = "size", bins = 100)

    ax.set_xlabel('Bins')
    ax.set_ylabel("Score")
    ax.set_title('"Deduct one" Range Size Frequency')

    ax.legend(fancybox = True, shadow = True)

    plt.show()

def main():
    data = pd.read_pickle("~/git/TLSHPasswordHash/dataCollection/dataframePickles/data.pkl")

    genHistogram(data)

    for p in prefix:
        cols = [p + suffix[0], p + suffix[1], p + suffix[2], p + suffix[3]]
        data[p + "Avg"] = data[cols].mean(axis = 1)
        print(data[cols].mean(axis = 1).mean())

    print(data["threeAvg"].mean() - data["oneAvg"].mean())




if __name__ == '__main__':
    main()