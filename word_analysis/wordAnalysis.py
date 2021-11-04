from math import log
import re
import pandas as pd

words = open("./words-by-frequency.txt").read().split()
wordcost = dict((k, log((i+1)*log(len(words)))) for i,k in enumerate(words))
maxword = max(len(x) for x in words)
wordStat = {}


def infer_spaces(s):

    def best_match(i):
        candidates = enumerate(reversed(cost[max(0, i-maxword):i]))
        return min((c + wordcost.get(s[i-k-1:i], 9e999), k+1) for k, c in candidates)

    cost = [0]
    for i in range(1, len(s)+1):
        c, k = best_match(i)
        cost.append(c)

    out = []
    i = len(s)
    while i > 0:
        c, k = best_match(i)
        assert c == cost[i]
        if k > 3:
            out.append(s[i-k:i])
        i -= k
    return out


def countWord(passwdList):
    wordStat = {}
    for s in passwdList:
        s = str(s)
        s = re.sub('[0-9’!"#$%&\'()*+,-./:;<=>?@，。?★、…【】《》？“”‘’！[\\]^_`{|}~\s]+', "", s)
        seglist = infer_spaces(s)
        for substr in seglist:
            if substr not in wordStat.keys():
                wordStat[substr] = 1
            else:
                wordStat[substr] += 1
    print('Word        Frequency')
    print('----------  -----------')
    for item, i in zip(sorted(wordStat.items(), key=lambda item: item[1], reverse=True), range(100)):
        key = item[0]
        value = item[1]
        print(key, end="")
        for j in range(10 - len(key) + 4):
            print(' ', end="")
        print(wordStat[key])


data = pd.read_csv('./Yahoo-original-mail-passwd.csv')
passwdList = pd.Series(data['passwd'].values)
countWord(passwdList)
