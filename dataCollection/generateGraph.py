import matplotlib
import matplotlib.pyplot as plt
from matplotlib.ticker import StrMethodFormatter
import matplotlib.font_manager as font_manager
import pandas as pd
import pickle
import numpy as np

prefix = ("one", "two", "three")
suffix = ("SubstituteDifference", "InsertDifference", "DeleteDifference", "CapitalizeDifference")

fontpath = '/usr/share/fonts/nerd-fonts-complete/otf/Fura Code Light Nerd Font Complete.otf'

fsize = (10, 7)

prop = font_manager.FontProperties(fname=fontpath)
matplotlib.rcParams['font.family'] = prop.get_name()

def axFormat (ax, title, xlabel, ylabel):
    # Despine
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['left'].set_visible(False)

    # Switch off ticks
    ax.tick_params(axis="both", which="both", bottom="off", top="off", labelbottom="on", left="off", right="off", labelleft="on")

    # Draw horizontal axis lines
    # vals = ax.get_yticks()
    # for tick in vals:
    #     ax.axhline(y=tick, linestyle='dashed', alpha=0.4, color='#eeeeee', zorder=1)

    # Remove title
    ax.set_title(title)

    # Set x-axis label
    ax.set_xlabel(xlabel, labelpad=20, weight='bold', size=12)

    # Set y-axis label
    ax.set_ylabel(ylabel, labelpad=20, weight='bold', size=12)

    # Format y-axis label
    ax.yaxis.set_major_formatter(StrMethodFormatter('{x:,g}'))

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

    fig, ax = plt.subplots(figsize=fsize)
    index = np.arange(len(oneError))
    barWidth = .2

    alignment = 'edge'

    oneBars = ax.bar(index - barWidth, oneError, barWidth, align = alignment, color = '#00D9C0', label = 'One Error', yerr = oneSEM)
    twoBars = ax.bar(index, twoError, barWidth, align = alignment, color = '#86BF91', label = 'Two Errors', yerr = twoSEM)
    threeBars = ax.bar(index + barWidth, threeError, barWidth, align = alignment, color = '#ADEEE3', label = "Three Errors", yerr = threeSEM)
    incorrectBars = ax.bar(index + barWidth*2, incorrectError, barWidth, align = alignment, color = '#B8D8D8', label = "Incorrect", yerr = incorrectSEM)

    title = 'Progression of Scores with increasing errors'
    xlabel = "Error Type"
    ylabel = "Score"

    axFormat(ax, title, xlabel, ylabel)

    ax.set_xticks(index + barWidth)
    ax.set_xticklabels(("Substituiton", "Insertion", "Deletion", "Capitalization"))

    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])

    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), fancybox=True, shadow=True)
    
    #plt.show()


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
            calcDF[s] = df["two" + suf].subtract(df["one" + suf]).divide(df["one" + suf]) * 100
        else:
            suf = suffix[i]
            calcDF[s] = ((df["three" + suf] - df["two" + suf]) / df["two" + suf]) * 100

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

    fig, ax = plt.subplots(figsize=fsize)
    index = np.arange(len(data12))
    barWidth = .4
    alignment = 'edge'

    apc12Label = u'1 → 2 error passwords'
    apc23Label = '2 ' + u"→" + ' 3 error passwords'

    apc12Bar = ax.bar(index, data12, barWidth, align = alignment, color = '#00D9C0', label = apc12Label, yerr = data12SEM)
    apc23Bar = ax.bar(index + barWidth, data23, barWidth, align = alignment, color = '#86BF91', label = apc23Label, yerr = data23SEM)

    title = 'Percent increase between passwords with different number of errors'
    xlabel = "Variations"
    ylabel = "Percentage"

    axFormat(ax, title, xlabel, ylabel)

    ax.set_xticks(index + barWidth)
    ax.set_xticklabels(("Substituiton", "Insertion", "Deletion", "Capitalization"))

    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])

    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), fancybox=True, shadow=True)
    
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

    fig, ax = plt.subplots(figsize=fsize)
    barWidth = .8
    alignment = 'center'

    lowerBar = ax.bar(1, lowerL[0], barWidth, color = '#00D9C0', label = "No deduction", yerr = lowerL[1])
    upperBar = ax.bar(1, upperL[0], barWidth, bottom = lowerL[0], color = '#86BF91', label = "Deduct one", yerr = upperL[1])
    topBar = ax.bar(1, 300 - lowerL[0] - upperL[0], barWidth, bottom = upperL[0] + lowerL[0], color = '#ADEEE3', label = 'Lower to two')
    leftBar = ax.bar(0, 0, .01)
    rightBar = ax.bar(2, 0, .01)

    title = 'Visualization of Score Range Use'
    xlabel = ""
    ylabel = "Score"

    axFormat(ax, title, xlabel, ylabel)

    ax.set_xticklabels([])
    ax.autoscale(enable = False, axis = 'x', tight = True)

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

    fig, ax = plt.subplots(figsize=fsize)
    index = np.arange(calcDF["upper"].size)
    
    ax.fill_between(calcDF["upper"], calcDF["lower"])

    title = 'Password Score Ranges'
    xlabel = "Password Number"
    ylabel = "Score"

    axFormat(ax, title, xlabel, ylabel)
    
    # ax.set_xticks(index + barWidth)
    # ax.set_xticklabels(index)
    ax.ticklabel_format(style='sci', axis='x', scilimits=(0,0))

    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), fancybox = True, shadow = True)

    # plt.show()

def genHistogram(df):
    calcDF = pd.DataFrame(dtype = np.float64)

    for p in prefix:
        cols = [p + suffix[0], p + suffix[1], p + suffix[2], p + suffix[3]]
        calcDF[p + "Avg"] = df[cols].mean(axis = 1)

    calcDF["average"] = calcDF[["oneAvg", "twoAvg", "threeAvg"]].mean(axis = 1)
    calcDF["stdev"] = calcDF[["oneAvg", "twoAvg", "threeAvg"]].std(axis = 1)
    calcDF["upper"] = calcDF["average"] + calcDF["stdev"]
    calcDF["lower"] = calcDF["average"] - calcDF["stdev"]
    calcDF["size"] = calcDF["upper"] - calcDF["lower"]

    print(calcDF["size"].mean())

    ax = calcDF.hist(column='size', label = "Number of ranges", bins = 24, range = (0, 250), grid=False, figsize=fsize, color='#00D9C0', rwidth = 1)

    title = '"Deduct One" Range Size Frequency'
    xlabel = "Size"
    ylabel = "Frequency"

    ax = ax[0]
    for x in ax:

        # Despine
        x.spines['right'].set_visible(False)
        x.spines['top'].set_visible(False)
        x.spines['left'].set_visible(False)

        # Switch off ticks
        x.tick_params(axis="both", which="both", bottom="off", top="off", labelbottom="on", left="off", right="off", labelleft="on")

        # Draw horizontal axis lines
        vals = x.get_yticks()
        for tick in vals:
            x.axhline(y=tick, linestyle='dashed', alpha=0.4, color='#eeeeee', zorder=1)

        # Remove title
        x.set_title(title)

        # Set x-axis label
        x.set_xlabel(xlabel, labelpad=20, weight='bold', size=12)

        # Set y-axis label
        x.set_ylabel(ylabel, labelpad=20, weight='bold', size=12)

        # Format y-axis label
        x.yaxis.set_major_formatter(StrMethodFormatter('{x:,g}'))
    
    #plt.show()

def main():
    data = pd.read_pickle("~/git/TLSHPasswordHash/dataCollection/dataframePickles/data.pkl")

    # genProgression(data)
    genPercentProgression(data)
    # genVisualizer(data)
    # genStock(data)
    # genHistogram(data)

    for p in prefix:
        cols = [p + suffix[0], p + suffix[1], p + suffix[2], p + suffix[3]]
        data[p + "Avg"] = data[cols].mean(axis = 1)
        print(data[cols].mean(axis = 1).mean())

    print(data["threeAvg"].mean() - data["oneAvg"].mean())

    print(data["incorrectDifference"].size)

    plt.show()


if __name__ == '__main__':
    main()