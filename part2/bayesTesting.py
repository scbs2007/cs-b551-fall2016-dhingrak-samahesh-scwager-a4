from __future__ import division
import os, string, math, heapq
from collections import Counter
import numpy as np
import cProfile


class TestingBayesModel:
    def __init__(self, directory):
        self.directory = directory

    def displayAccuracy(self, confidenceMatrix):
        print "\n\nAccuracy Percentage: ", np.trace(confidenceMatrix) / np.sum(confidenceMatrix)
        print "Confusion matrix:"
        s = ""
        for i in range(20):
            for j in range(20):
                s += str(confidenceMatrix[i,j]) + "\t"
            s += "\n"
        print s
                
    def calculateProbWordsGivenTopic(self, probWGivenT, wordCount, pClass):
#         Takes into account the case where no words are in probWGivenT, i.e. probKnowTopic is zero or nearly zero
        return sum([math.log(probWGivenT[entry]) if entry in wordCount else \
        math.log(1 - probWGivenT[entry]) if probWGivenT[entry] > 0 else 0 for entry in probWGivenT]) + math.log(pClass)   
                      
    def testModelHelp(self, currTopicIndex, topicList, probTopic, probWord, probWGivenTopic, confidenceMatrix, fetchTokens, topicName, directoryPath):
        counter = 0
        for fileName in os.listdir(directoryPath):
            if counter > 20: return
            counter += 1
            with open(directoryPath + '/' + fileName) as document:
                wordSet = set( fetchTokens(document) )
                prob, idx = -100000, -1
                for i, (topic, topicDir) in enumerate(topicList):
                    p =  self.calculateProbWordsGivenTopic(probWGivenTopic[topic], wordSet, probTopic[topic])
                    if p > prob: 
                        prob, idx = p, i
            confidenceMatrix[currTopicIndex, idx] += 1

    def testModel(self, probTopic, probWord, probWGivenTopic, confidenceMatrix, fetchTokens):
        topics = [(topicName, os.path.join(self.directory, topicName)) for topicName in os.listdir(self.directory) if os.path.isdir(os.path.join(self.directory, topicName))]
        for i, (topic, topicDir) in enumerate(topics):
            self.testModelHelp(i, topics, probTopic, probWord, probWGivenTopic, confidenceMatrix, fetchTokens, topic, topicDir)
                                                 
    def testDocuments(self, modelObj):
        probTopic = modelObj.probTopic
        probWord = modelObj.probWord
        probWGivenTopic_Bernoulli = modelObj.probWGivenTopic_Bernoulli

        confidenceMatrix_Bernoulli = np.zeros((20,20))

        # Testing each topic folder
        self.testModel(probTopic, probWord, probWGivenTopic_Bernoulli, confidenceMatrix_Bernoulli, modelObj.processCorpus.fetchTokens)
        
        self.displayAccuracy(confidenceMatrix_Bernoulli)



