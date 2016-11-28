from __future__ import division
import os, string, sys, math, pickle, re
from collections import Counter
from processCorpus import ProcessCorpus
from processCorpusUnknown import ProcessCorpusUnknown

class TrainingBayesModel:
    def __init__(self, directory, probKnowTopic = 1.):
        self.directory = directory
        self.probKnowTopic = probKnowTopic
        self.processCorpus = ProcessCorpusUnknown("./train", self.probKnowTopic)
        self.totTrainingDocs = 0
        self.docTopics = {} #probability of each of the 20 topics
        
    def calculateProbWordsGivenTopic(self, probWGivenT, wordCount, pClass):
        # For now considering only words present in the training data.
        return sum([math.log(probWGivenT[entry]) for entry in wordCount if entry in probWGivenT]) + math.log(pClass)
        
    def calculateProbWGivenTopic_Multinomial(self, wordCount, totWordsInClass, totDocs):
        prob = Counter()
        for entry in wordCount:
            prob[entry] = wordCount[entry]/(totWordsInClass + totDocs)
        return prob
        
    def calculateProbWGivenTopics_Multinomial(self, wordCountInTopics, totDocWordCountInTopics, totDocs):
        probWGivenTopic = Counter()
        for topic in wordCountInTopics:
            totWordsInTopic = totDocWordCountInTopics[topic][1] #number of words in topic
            probWGivenTopic[topic] = self.calculateProbWGivenTopic_Multinomial(wordCountInTopics[topic], totWordsInTopic, totDocs)
        return probWGivenTopic
        
    def assignTopicsToUnknown(self, wordCountInTopics, wordCountInEachDoc, totDocWordCountInTopics, topicIsFixed, probWGivenT, totDocs): 
        '''assign max prob topic to each doc whose topic is unknown
        TO DO: assign randomly when the number of docs with known topics is small or zero'''
        for docID, (fixed, topicID) in topicIsFixed.items():
            if not fixed:
                wordCountInDoc = wordCountInEachDoc[docID]
                highestProbTopic, prob = "", -100000
                for topic, wordCount in wordCountInTopics.items():
                    #docCount = totDocWordCountInTopics[topic][0] #TO DO?? number of docs in topic ??need to check whether to use this or totDocs
                    probTopicGivenDoc = self.calculateProbWordsGivenTopic(probWGivenT, wordCount, totDocs)
                    if probTopicGivenDoc > prob:
                        highestProbTopic, prob = topic, probTopicGivenDoc
                topicIsFixed[docID] = (False, highestProbTopic)
        
    def calculateProbTopic(self, totDocWordCountInTopics, totalDocs):
        '''probability of a given topic occurring, calculated based on number of examples for each topic'''
        prob = Counter()
        for entry in totDocWordCountInTopics:
            docCount = totDocWordCountInTopics[entry][0]
            prob[entry] = docCount/totalDocs
            #print docCount, totalDocs, prob[entry]
        return prob

    def train(self): 
        print "Training Bayes Net Model."
        print "Creating Vector."
        self.processCorpus.calculate()

        wordCountInTopics = self.processCorpus.wordCountMapping # stores key = topic name, value = Counter object reference (count of each word's occurrence in all docs combined)
        totDocWordCountInTopics = self.processCorpus.docsAndWords # stores the number of words and the number of documents for all topics as tuples.
        topicIsFixed = self.processCorpus.topicIsFixed #stores key = document ID, value = tuple: topic, whether topic was known in advance or only estimated
        wordCountInEachDoc = self.processCorpus.wordCountInEachDoc # stores key: doc ID, value = counter object reference for the doc 
        totalDocs = self.processCorpus.totalDocs #total number of docs
        
        self.probWGivenTopic_Multinomial = self.calculateProbWGivenTopics_Multinomial(wordCountInTopics, totDocWordCountInTopics, totalDocs)
        print "before\n\n"
        print topicIsFixed
        self.assignTopicsToUnknown(wordCountInTopics, wordCountInEachDoc, totDocWordCountInTopics, topicIsFixed, self.probWGivenTopic_Multinomial, totalDocs)
        print "after\n\n"
        print topicIsFixed


        

    
