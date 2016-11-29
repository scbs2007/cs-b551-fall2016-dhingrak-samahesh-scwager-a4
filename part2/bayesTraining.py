from __future__ import division
import os, string, sys, math, pickle, re
from collections import Counter
from processCorpusUnknown import ProcessCorpusUnknown

class TrainingBayesModel:
    def __init__(self, directory, probKnowTopic = 1.):
        self.directory = directory
        self.probKnowTopic = probKnowTopic
        self.processCorpus = ProcessCorpusUnknown("./train", self.probKnowTopic)
        self.totTrainingDocs = 0
        self.docTopics = {} #probability of each of the 20 topics
        self.probWGivenTopic_Multinomial = {} #probability of each word given each topic
        
    def calculateProbWGivenTopic_Multinomial(self, wordCount, totWordsInClass):
        '''returns counter object reference for single topic'''
        prob = Counter()
        for entry in wordCount:
            prob[entry] = (wordCount[entry]+1)/(totWordsInClass+1)
        return prob
        
    def calculateProbWGivenTopics_Multinomial(self, wordCountInTopics, totDocWordCountInTopics):
        '''returns a counter with key: topic, value: counter object reference: probability of each word'''
        probWGivenTopic = Counter()
        for topic in wordCountInTopics:
            totWordsInTopic = totDocWordCountInTopics[topic][1] #total number of words in topic
            probWGivenTopic[topic] = self.calculateProbWGivenTopic_Multinomial(wordCountInTopics[topic], totWordsInTopic) #prob of each word occurring in topic
        return probWGivenTopic
        
    def calculateProbWordsGivenTopic(self, probWGivenT, wordCount, pClass):
        # For now considering only words present in the training data.
        return sum([math.log(probWGivenT[entry]) for entry in wordCount if entry in probWGivenT]) + math.log(pClass)
        
    def assignTopicsToUnknown(self, wordCountInEachDoc, topicIsFixed, probWGivenTopic, probTopic): 
        '''assign max prob topic to each doc whose topic is unknown
        TO DO: assign randomly when the number of docs with known topics is small or zero'''
        for docID, (fixed, topicID) in topicIsFixed.items():
            if not fixed or fixed: #remove or if fixed
                wordCountInDoc = wordCountInEachDoc[docID]
                highestProbTopic, prob = "", -100000
                for topic, probT in probTopic.items():
                    probTopicGivenDoc = self.calculateProbWordsGivenTopic(probWGivenTopic[topic], wordCountInDoc, probT)
                    if probTopicGivenDoc > prob:
                        highestProbTopic, prob = topic, probTopicGivenDoc
#                         print "highestProbTopic", highestProbTopic, "prob", prob
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
        wordCountInEachDoc = self.processCorpus.wordCountInEachDoc # stores key: doc ID, value = counter object reference for the doc (counts only docs with *known* topic)
        totalDocs = self.processCorpus.totalDocs #total number of docs with *known* topic because used for the prob calculation
        probTopic = self.calculateProbTopic(totDocWordCountInTopics, totalDocs)
        
        self.probWGivenTopic_Multinomial = self.calculateProbWGivenTopics_Multinomial(wordCountInTopics, totDocWordCountInTopics)
        print "before\n\n"
        counter = 0
        for entry, (fixed, topic) in topicIsFixed.items():
            if counter < 100 and not fixed:
              print entry, fixed, topic
            counter += 1
        self.assignTopicsToUnknown(wordCountInEachDoc, topicIsFixed, self.probWGivenTopic_Multinomial, probTopic)
        print "after\n\n"
        counter = 0
        for entry, (fixed, topic) in topicIsFixed.items():
            if counter < 100 and not fixed:
              print entry, fixed, topic
            counter += 1


        

    
