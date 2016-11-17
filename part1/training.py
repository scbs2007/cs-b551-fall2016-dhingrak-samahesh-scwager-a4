from __future__ import division
import os, string, sys, math, pickle
from collections import Counter

class TrainModel:
    def __init__(self, directory):
        self.directory = directory
        
        self.pSpam = 0
        self.pNotSpam = 0
        self.probWGivenNotSpam_Bernoulli = Counter()
        self.probWGivenSpam_Bernoulli = Counter()

        self.probWGivenNotSpam_Multinomial = Counter()
        self.probWGivenSpam_Multinomial = Counter()        

    def fetchTokens(self, document):
        # Currently considering words after splitting on space and removing all punctuations.
        # TODO - Improve word check. words to use (not number, URL)
        return [token.translate(None, string.punctuation) for token in document.read().split()]

    # Counts w|c for both bernoulli and multinomial; total number of words in a document
    def countWordsInDocument(self, wordFreqMultinomial, wordFreqBernoulli, document):
        flag = set() # Keeps track of word that has already been counted once for a particular document - For Bernoulli Model
        count = 0 # Counts total number of words in document
        for entry in self.fetchTokens(document):
            if entry != '':
                count += 1
                wordFreqMultinomial[entry] += 1
                if entry in flag:
                    continue
                wordFreqBernoulli[entry] += 1
                flag.add(entry)
        return count

    def creatingVector(self, wordFreqMultinomial, wordFreqBernoulli, classType):
        docCount = 0 # Total spam/non spam documents in training data
        wordCount = 0 # Count of words in class
        # Reading all files in train directory
        directoryPath = self.directory + '/train/' + classType
                        #os.getcwd() + '/train/' + classType
        for fileName in os.listdir(directoryPath):
            with open(directoryPath + '/' + fileName) as document:
                wordCount += self.countWordsInDocument(wordFreqMultinomial, wordFreqBernoulli, document)
                docCount += 1
            #print "File: ", fileName
            #for entry in wordCountInDocs:
            #    print entry, wordCountInDocs[entry]
        return docCount, wordCount

    def calculateProbWGivenClass_Multinomial(self, wordCount, totWordsInClass, totDocs):
        prob = Counter()
        for entry in wordCount:
            prob[entry] = wordCount[entry]/(totWordsInClass + totDocs)
            #if prob[entry] == 0:
            #    print entry, prob[entry]
        return prob
    
    def calculateProbWGivenClass_Bernoulli(self, wordCount, docCount):
        prob = Counter()
        for entry in wordCount:
            prob[entry] = wordCount[entry]/docCount
            #if prob[entry] == 0:
            #    print entry, prob[entry]
        return prob
    
    def increaseCountForWords(self, count):
        #temp = count
        #increment = 1
        #print "Before: ", count
        #count = Counter(dict.fromkeys(temp, increment))
        #print "After: ", count
        for entry in count:
            count[entry] += 1
    
    # Adds words missing in class2 but present in class1, to class2 with count 1
    def addWord(self, count1, count2):
        count1keys = count1.elements()
        count2keys = count2.elements()
        for entry in count1keys:
            if entry not in count2keys:
                count2[entry] = 0 
        #print "BEFORE: ", count2
        self.increaseCountForWords(count2) #Adding 1 to all counts
        #print "AFTER: ", count2
    
    def smoothCounts(self, wordCountInSpam_Multinomial, wordCountInNotSpam_Multinomial, wordCountInSpam_Bernoulli, wordCountInNotSpam_Bernoulli):
        print "Smoothing."
        self.addWord(wordCountInNotSpam_Multinomial, wordCountInSpam_Multinomial)
        self.addWord(wordCountInSpam_Multinomial, wordCountInNotSpam_Multinomial)
        self.increaseCountForWords(wordCountInSpam_Bernoulli)
        self.increaseCountForWords(wordCountInNotSpam_Bernoulli)
    
    def train(self): 
        print "Training Model."
        # Key = Word, Value = Count of the documents which contain the word
        wordCountInNotSpam_Bernoulli = Counter()
        wordCountInSpam_Bernoulli = Counter() 
        
        # Key = Word, Value = Number of occurences in training data 
        wordCountInNotSpam_Multinomial = Counter()
        wordCountInSpam_Multinomial = Counter() 
        
        print "Creating Vector."
        totNotSpamDocs, totWordsInNotSpam = self.creatingVector(wordCountInNotSpam_Multinomial, wordCountInNotSpam_Bernoulli, 'notspam')
        totSpamDocs, totWordsInSpam = self.creatingVector(wordCountInSpam_Multinomial, wordCountInSpam_Bernoulli, 'spam')
        # + 2 for smoothing
        totSpamDocs += 2
        totNotSpamDocs += 2
        totTrainingDocs = totNotSpamDocs + totSpamDocs
        
        self.smoothCounts(wordCountInNotSpam_Multinomial, wordCountInSpam_Multinomial, wordCountInSpam_Bernoulli, wordCountInNotSpam_Bernoulli)
        #print "Spam Multinomial", wordCountInNotSpam_Multinomial['Received'], "NonSpam Multinomial", wordCountInSpam_Multinomial['Received']
        #print "Spam Bernoulli", wordCountInSpam_Bernoulli['Received'], "NonSpam Bernoulli: ", wordCountInNotSpam_Bernoulli['Received']
        self.probWGivenNotSpam_Bernoulli = self.calculateProbWGivenClass_Bernoulli(wordCountInNotSpam_Bernoulli, totNotSpamDocs)
        self.probWGivenSpam_Bernoulli = self.calculateProbWGivenClass_Bernoulli(wordCountInSpam_Bernoulli, totSpamDocs)
        
        self.probWGivenNotSpam_Multinomial = self.calculateProbWGivenClass_Multinomial(wordCountInNotSpam_Multinomial, totWordsInNotSpam, totTrainingDocs)
        self.probWGivenSpam_Multinomial = self.calculateProbWGivenClass_Multinomial(wordCountInSpam_Multinomial, totWordsInSpam, totTrainingDocs)
        #print "NOT SPAM B: ", probWGivenNotSpam_Bernoulli
        #print "\nSPAM B: ", probWGivenSpam_Bernoulli
        #print "\nNOT SPAM M: ", probWGivenNotSpam_Multinomial
        #print "\nSPAM M:", probWGivenSpam_Multinomial
        
        #print probWGivenNotSpam_Bernoulli['Received'], probWGivenSpam_Bernoulli['Received'], probWGivenNotSpam_Multinomial['Received'], probWGivenSpam_Multinomial['Received']
        self.pSpam = totSpamDocs / (totSpamDocs + totNotSpamDocs)
        self.pNotSpam = totNotSpamDocs / (totSpamDocs + totNotSpamDocs)

