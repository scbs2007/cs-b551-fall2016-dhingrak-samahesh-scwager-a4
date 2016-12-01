from __future__ import division
import os, string, math, heapq
from collections import Counter


class TestingBayesModel:
    def __init__(self, directory):
        self.directory = directory

    def displayAccuracy(self, confidenceMatrix):
        print "\n\nAccuracy Percentage: ", round((confidenceMatrix[0] + confidenceMatrix[3]) * 100.0 / sum(confidenceMatrix), 2)
        print "Confidence Matrix: "
        print "True Positive: ", confidenceMatrix[0]
        print "False Negative: ", confidenceMatrix[1] 
        print "False Positive: ", confidenceMatrix[2] 
        print "True Negative: ", confidenceMatrix[3] 

    def calculateProbWordsGivenTopic(self, probWGivenT, wordCount, pClass):
        # For now considering only words present in the training data.
        # Also for a particular test document's words - taking into consideration only P(W|S) and not 1 - P(W|S)
        return sum([math.log(probWGivenT[entry]) for entry in wordCount if entry in probWGivenT]) + math.log(pClass)

    def bernoulliThresh(self, oddsRatio, confidenceMatrix, threshold, classType):
        if oddsRatio > threshold:
            #print "Predicted - Spam"
            if classType == 'spam':
                confidenceMatrix[0] += 1
            if classType == 'notspam':
                confidenceMatrix[1] += 1
        else:
            #print "Predicted - Not Spam"
            if classType == 'spam':
                confidenceMatrix[2] += 1
            if classType == 'notspam':
                confidenceMatrix[3] += 1

    def testModel(self, probTopic, probWord, probWGivenTopic, confidenceMatrix, fetchTokens):
        probTGivenW = Counter()
        topics = [os.path.join(self.directory, topicName) for topicName in os.listdir(self.directory) if os.path.isdir(os.path.join(self.directory, topicName))]
        for topic in topics:
            return
        for fileName in os.listdir(directoryPath):
            with open(directoryPath + '/' + fileName) as document:
                wordList = set( fetchTokens(document) ) #TO DO: check that using "set" is correct: don't want to count the same word multiple times
                    for topic in probTopic:
                        probTGivenW[topic] =  self.calculateProbWordsGivenTopic(probWGivenTopic, wordList, probTopic)
              
                #print "\nFile Name: ", fileName, "Type: ", classType
                                                 
    def testDocuments(self, modelObj):
        probTopic = modelObj.probTopic
        probWord = modelObj.probWord
        probWGivenTopic_Bernoulli = modelObj.probWGivenTopic_Bernoulli

        # 0 - true positive, 1 - false negative, 2 - false positive, 3 - true negative
        confidenceMatrix_Bernoulli = np.zeros((20,20))

        # Testing each topic folder
        self.testModel(probTopic, probWord, probWGivenTopic, confidenceMatrix_Bernoulli, modelObj.processCorpusUnknown.fetchTokens)
        self.displayAccuracy(confidenceMatrix_Bernoulli)



