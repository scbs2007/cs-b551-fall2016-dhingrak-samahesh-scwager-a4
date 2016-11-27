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
        self.probTopic = {} #probability of each of the 20 topics
        self.probWGivenTopic = {} #each list item is a counter for one topic
    
    def calculateProbWGivenTopic(self, wordCount, docCount):
        prob = Counter()
        for entry in wordCount:
            prob[entry] = wordCount[entry]/docCount
        return prob
        
    def calculateProbWGivenTopics(self, wordCountInTopics, totDocWordCountInTopics): 
    #TO DO: currently uses doc counts. do we also need to use word counts? wordCount = totDocWordCountInTopics[key][1]
        probWGivenTopic = {} #
        for topic, wordCount in wordCountInTopics.items():
            docCount = totDocWordCountInTopics[topic][0]
            probWGivenTopic[topic] = self.calculateProbWGivenTopic(wordCount, docCount)
        return probWGivenTopic
        
    def calculateProbTopic(self, totDocWordCountInTopics, totalDocs):
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
        totalDocs = self.processCorpus.totalDocs
        
        self.probWGivenTopic = self.calculateProbWGivenTopics(wordCountInTopics, totDocWordCountInTopics) #stores key = topic name, value = p of word given the topic
        self.probTopic = self.calculateProbTopic(totDocWordCountInTopics, totalDocs) #key = topic, value = probability of the topic       

        

    
