import math
import csv
import pprint

csvFile = "test.csv"
searchPhrase = "Word1 Word2"

def calculateBm25(phrase, document, corpus):
    k = 1.2
    b = .75
    
    averageDocLength = getAvereageDocLength(corpus)

    # IDF, DF, TF, N, L
    phraseList = phrase.split()
    N = len(phraseList)
    subBM25List = list()

    for subPhrase in phraseList:
        TF = document["FrequencyOf"+subPhrase]
        DF = getDF(subPhrase, corpus)
        IDF = getIDF(len(corpus), DF)
        subBM25 = IDF * ((TF * (k + 1))/(TF + k*(1 - b + b*(document["DocumentL"]/averageDocLength))))
        subBM25List.append(subBM25)

    BM25 = sum(subBM25List)
    return BM25

def getAvereageDocLength(corpus):
    documentLengthSum = 0
    for document in corpus:
        documentLengthSum += document["DocumentL"]
    
    return documentLengthSum/len(corpus)

def getDF(phrase, corpus):
    DF = 0
    for document in corpus:
        if document["FrequencyOf"+phrase] > 0:
            DF += 1
    return DF

def getIDF(N, DF):
    return math.log((N - DF + 0.5)/(DF + 0.5))

def getRank(rankDict):
    return rankDict["BM25"]


# begin script

# import csv as list of dictionaries
with open(csvFile) as file:
    corpus = [{k: int(v) for k, v in row.items()}
        for row in csv.DictReader(file, skipinitialspace=True)]
    
rankList = []

for document in corpus:
    BM25 = calculateBm25(searchPhrase, document, corpus)
    rankList.append({
        "DocumentID": document["DocumentID"],
        "BM25": BM25
    })

rankList.sort(key=getRank)

print("Document Rank")
pprint.pp(rankList)