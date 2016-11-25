from __future__ import division
import math
from binaryNode import BinaryNode
from numpy import *

class BinaryTree:
    def __init__(self, processCorpus, spamDocuments, notSpamDocuments):
        self.processCorpus = processCorpus
        self.root = None
        self.wordCountNotSpam = processCorpus.wordCountInNotSpam_Bernoulli 
        self.wordCountSpam = processCorpus.wordCountInSpam_Bernoulli
        self.totTrainingDocs = processCorpus.totTrainingDocs 
        self.totSpamDocs = processCorpus.totSpamDocs
        self.totNotSpamDocs = processCorpus.totNotSpamDocs
        
        self.wordList = processCorpus.allWordsInCorpus #list with all the words in all emails
        '''
        each list element contains a counter dict for each word in a given document.
        for bernoulli, simply check whether word is in the counter dict. for multinomial, look at the word's value
        '''
        self.documentDictListSpam = spamDocuments 
        self.documentDictListNotSpam = notSpamDocuments

    def dtLearning(self, maxHeight = 2):
        print "Training Binary Decision Tree Model."
        rootWord = self.mostImportantWord()
        self.root = BinaryNode(attribute = rootWord)
        
        #print self.documentDictListSpam[0]
        
        self.root.left = dtleftCondition = {rootWord: 0}
        rightCondition = {rootWord: 1}
        print "root of binary tree", rootWord
        return self.root

    def dtLearningHelp(self, condition, remainingHeight):
        return

    def mostImportantWord(self, condition = {}): 
        bestWord, bestEntropy = "", 1.1
        for word in self.wordList:
            totalPresentSpam = totalNotPresentSpam = totalPresentNonSpam = totalNotPresentNonSpam = 1 #add 1 for smoothing
#             do to: add statement: if condition holds (e.g. word1 is not in document, word2 is in document, word3, ...etc)
#             so that only the words that are on this branch are counted
            for doc in self.documentDictListNotSpam: #loop through all documents which are not spam
                if word in doc and check_condition(doc, condition): totalPresentNonSpam += 1 #count how many have the word
                else: totalNotPresentNonSpam += 1 #count how many don't have the word
            for doc in self.documentDictListSpam: #loop through all documents which are spam
                if word in doc and check_condition(doc, condition): totalPresentSpam += 1
                else: totalNotPresentSpam += 1

            entropy = self.calculateEntropy(totalPresentSpam, totalNotPresentSpam, totalPresentNonSpam, totalNotPresentNonSpam)
            
#             print "word", word, "entropy", entropy
            if entropy < bestEntropy:
                bestWord, bestEntropy = word, entropy
        return bestWord, bestEntropy
        
    def check_condition(doc, condition):
        for word, isInDoc in condition.items():
            if word in doc and not isInDoc or word not in doc and isInDoc:
                return False
        return True  
            
    def entropy_Bernoulli(self, positiveCount, totalCount):
        p = positiveCount/totalCount
        return  -(p*log2(p) + (1-p)*log2(1-p))
        
    def calculateEntropy(self, totalPresentSpam, totalNotPresentSpam, totalPresentNonSpam, totalNotPresentNonSpam):
        totalPresent = totalPresentNonSpam + totalPresentSpam #pk1 + nk1, 1: contains word
        totalNotPresent = totalNotPresentNonSpam + totalNotPresentSpam #pk2 + nk2
        totalDocs = totalPresent + totalNotPresent
        return ( totalPresent / totalDocs * self.entropy_Bernoulli(totalPresentNonSpam, totalPresent) +
                 totalNotPresent / totalDocs * self.entropy_Bernoulli(totalNotPresentNonSpam, totalNotPresent) )
        
    '''
        def calculateEntropy(self, word, totalPresent, totalNotPresentSpam, totalNotPresentNonSpam, totalNotPresent):

            entropy = totalPresent / self.totTrainingDocs * (- self.wordCountNotSpam[word]/totalPresent * log (self.wordCountNotSpam[word]/ totalPresent)
                                     - self.wordCountSpam[word]/totalPresent * log (self.wordCountSpam[word]/ totalPresent)
                                    ) 
                                    +
                 totalNotPresent / self.totTrainingDocs *	(- totalNotPresentSpam/totalNotPresent * log (totalNotPresentSpam/totalNotPresent)
                                     - totalNotPresentNonSpam/totalNotPresent * log (totalNotPresentSpam/totalNotPresent)
                                    )              
            return entropy  
                    
    #         and you get self.whatever from the bayes object
    '''
        
