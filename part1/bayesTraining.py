from __future__ import division
import os, string, sys, math, pickle, re
from collections import Counter
from processCorpus import ProcessCorpus

class TrainingBayesModel:
    def __init__(self, directory):
        self.directory = directory
        self.processCorpus = ProcessCorpus(directory)
        self.totTrainingDocs = 0
        self.pSpam = 0
        self.pNotSpam = 0
        self.probWGivenNotSpam_Bernoulli = Counter()
        self.probWGivenSpam_Bernoulli = Counter()

        self.probWGivenNotSpam_Multinomial = Counter()
        self.probWGivenSpam_Multinomial = Counter()

    def calculateProbWGivenClass_Multinomial(self, wordCount, totWordsInClass, totDocs):
        prob = Counter()
        for entry in wordCount:
            prob[entry] = wordCount[entry]/(totWordsInClass + totDocs)
        return prob
    
    def calculateProbWGivenClass_Bernoulli(self, wordCount, docCount):
        prob = Counter()
        for entry in wordCount:
            prob[entry] = wordCount[entry]/docCount
        return prob

    def train(self): 
        print "Training Bayes Model."
        print "Creating Vector."
        self.processCorpus.calculate()

        totSpamDocs = self.processCorpus.totSpamDocs
        totNotSpamDocs = self.processCorpus.totNotSpamDocs
        totTrainingDocs = self.processCorpus.totTrainingDocs

        totWordsInSpam = self.processCorpus.totWordsInSpam
        totWordsInNotSpam = self.processCorpus.totWordsInNotSpam

        wordCountInNotSpam_Bernoulli = self.processCorpus.wordCountInNotSpam_Bernoulli
        wordCountInSpam_Bernoulli = self.processCorpus.wordCountInSpam_Bernoulli
        wordCountInNotSpam_Multinomial = self.processCorpus.wordCountInNotSpam_Multinomial
        wordCountInSpam_Multinomial = self.processCorpus.wordCountInSpam_Multinomial
        
        self.probWGivenNotSpam_Bernoulli = self.calculateProbWGivenClass_Bernoulli(wordCountInNotSpam_Bernoulli, totNotSpamDocs)
        self.probWGivenSpam_Bernoulli = self.calculateProbWGivenClass_Bernoulli(wordCountInSpam_Bernoulli, totSpamDocs)
        
        self.probWGivenNotSpam_Multinomial = self.calculateProbWGivenClass_Multinomial(wordCountInNotSpam_Multinomial, totWordsInNotSpam, totTrainingDocs)
        self.probWGivenSpam_Multinomial = self.calculateProbWGivenClass_Multinomial(wordCountInSpam_Multinomial, totWordsInSpam, totTrainingDocs)
        
        self.pSpam = totSpamDocs / (totSpamDocs + totNotSpamDocs)
        self.pNotSpam = totNotSpamDocs / (totSpamDocs + totNotSpamDocs)

