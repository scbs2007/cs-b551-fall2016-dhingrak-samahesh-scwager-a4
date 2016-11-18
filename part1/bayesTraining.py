from __future__ import division
import os, string, sys, math, pickle
from collections import Counter
import re

class TrainingBayesModel:
    def __init__(self, directory):
        self.directory = directory
        self.totTrainingDocs = 0
        self.pSpam = 0
        self.pNotSpam = 0
        self.probWGivenNotSpam_Bernoulli = Counter()
        self.probWGivenSpam_Bernoulli = Counter()

        self.probWGivenNotSpam_Multinomial = Counter()
        self.probWGivenSpam_Multinomial = Counter()

        # Key = Word, Value = Count of the documents which contain the word
        self.wordCountInNotSpam_Bernoulli = Counter()
        self.wordCountInSpam_Bernoulli = Counter() 
        
        # Key = Word, Value = Number of occurences in training data 
        self.wordCountInNotSpam_Multinomial = Counter()
        self.wordCountInSpam_Multinomial = Counter() 

    def fetchTokens(self, document):
        # Currently considering words after splitting on space and removing all punctuations. all lower case.
        # TODO - Improve word check. words to use (not number, URL)
        return [str.lower(token.translate(None, string.punctuation)) for token in document.read().split()]

    # Counts w|c for both bernoulli and multinomial; total number of words in a document
    def countWordsInDocument(self, wordFreqMultinomial, wordFreqBernoulli, document):
        flag = set() # Keeps track of word that has already been counted once for a particular document - For Bernoulli Model
        count = 0 # Counts total number of words in document
        for entry in self.fetchTokens(document):
            if entry != '' and re.match("^[\w\d_-]*$", entry):
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
        #self.addWord(wordCountInNotSpam_Multinomial, wordCountInSpam_Multinomial)
        #self.addWord(wordCountInSpam_Multinomial, wordCountInNotSpam_Multinomial)
        self.increaseCountForWords(wordCountInSpam_Bernoulli)
        self.increaseCountForWords(wordCountInNotSpam_Bernoulli)
        self.increaseCountForWords(wordCountInSpam_Multinomial)
        self.increaseCountForWords(wordCountInNotSpam_Multinomial)
    
    # Removing words with frequency lower than 5 from consideration
    def removeLowFreqWords(self, wordCount):
         for entry in wordCount.keys():
            if wordCount[entry] < 6:
                del wordCount[entry]
   
    def lowFrequency(self):
        self.removeLowFreqWords(self.wordCountInNotSpam_Multinomial)
        self.removeLowFreqWords(self.wordCountInSpam_Multinomial)
        self.removeLowFreqWords(self.wordCountInSpam_Bernoulli)
        self.removeLowFreqWords(self.wordCountInNotSpam_Bernoulli)
         
    '''
    def wordsContainingNumbers(self):

    def numbers(self):
        self.wordsContainingNumbers(self.wordCountInNotSpam_Multinomial)
        self.wordsContainingNumbers(self.wordCountInSpam_Multinomial)
        self.wordsContainingNumbers(self.wordCountInSpam_Bernoulli)
        self.wordsContainingNumbers(self.wordCountInNotSpam_Bernoulli)
    '''    

    def removeWordsFromConsideration(self):
        self.lowFrequency()
        #self.numbers()

    def train(self): 
        print "Training Model."
        print "Creating Vector."
        totNotSpamDocs, totWordsInNotSpam = self.creatingVector(self.wordCountInNotSpam_Multinomial, self.wordCountInNotSpam_Bernoulli, 'notspam')
        totSpamDocs, totWordsInSpam = self.creatingVector(self.wordCountInSpam_Multinomial, self.wordCountInSpam_Bernoulli, 'spam')
        # + 2 for smoothing
        totSpamDocs += 2
        totNotSpamDocs += 2
        self.totTrainingDocs = totNotSpamDocs + totSpamDocs
        
        self.smoothCounts(self.wordCountInNotSpam_Multinomial, self.wordCountInSpam_Multinomial, self.wordCountInSpam_Bernoulli, self.wordCountInNotSpam_Bernoulli)
        #print "Spam Multinomial", self.wordCountInNotSpam_Multinomial['Received'], "NonSpam Multinomial", self.wordCountInSpam_Multinomial['Received']
        #print "Spam Bernoulli", self.wordCountInSpam_Bernoulli['Received'], "NonSpam Bernoulli: ", self.wordCountInNotSpam_Bernoulli['Received']
        self.removeWordsFromConsideration()

        self.probWGivenNotSpam_Bernoulli = self.calculateProbWGivenClass_Bernoulli(self.wordCountInNotSpam_Bernoulli, totNotSpamDocs)
        self.probWGivenSpam_Bernoulli = self.calculateProbWGivenClass_Bernoulli(self.wordCountInSpam_Bernoulli, totSpamDocs)
        
        self.probWGivenNotSpam_Multinomial = self.calculateProbWGivenClass_Multinomial(self.wordCountInNotSpam_Multinomial, totWordsInNotSpam, self.totTrainingDocs)
        self.probWGivenSpam_Multinomial = self.calculateProbWGivenClass_Multinomial(self.wordCountInSpam_Multinomial, totWordsInSpam, self.totTrainingDocs)
        #print "NOT SPAM B: ", probWGivenNotSpam_Bernoulli
        #print "\nSPAM B: ", probWGivenSpam_Bernoulli
        #print "\nNOT SPAM M: ", probWGivenNotSpam_Multinomial
        #print "\nSPAM M:", probWGivenSpam_Multinomial
        
        #print probWGivenNotSpam_Bernoulli['Received'], probWGivenSpam_Bernoulli['Received'], probWGivenNotSpam_Multinomial['Received'], probWGivenSpam_Multinomial['Received']
        self.pSpam = totSpamDocs / (totSpamDocs + totNotSpamDocs)
        self.pNotSpam = totNotSpamDocs / (totSpamDocs + totNotSpamDocs)

