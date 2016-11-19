from __future__ import division
import math
from binaryNode import BinaryNode

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

    def dtLearning(self, maxHeight = 1):
        print "Training Binary Decision Tree Model."
        rootWord = self.mostImportantWord()
        self.root = BinaryNode(attribute = rootWord)
        
        #print self.documentDictListSpam[0]
        
        leftCondition = {rootWord: 0}
        rightCondition = {rootWord: 1}
        return self.root

    def dtLearningHelp(self, condition, remainingHeight):
        return

    def mostImportantWord(self, condition = {}): 
        bestWord, entropy = "", 1.1
        for word in self.wordList:
            positiveCountSpam = negativeCountSpam = positiveCountNotSpam = negativeCountNotSpam = 0
            '''
            do to: add statement: if condition holds (e.g. word1 is not in document, word2 is in document, word3, ...etc)
            so that only the words that are on this branch are counted
            documentDictListSpam: each list element contains a counter dict for each word in a given document.
            for bernoulli, simply check whether word is in the counter dict. for multinomial, look at the word's value
            '''
            if word in self.documentDictListNotSpam: positiveCountNotSpam += 1
            else: negativeCountNotSpam += 1
            if word in self.documentDictListSpam: positiveCountSpam += 1
            else: negativeCountSpam += 1
            
            '''
            next, calculate entropy in the left and right branches. replace bestWord and entropy if the current value is 
            better
            '''
        #self.calculateEntropy("to")
        pass
            
    def entropy_Bernoulli(self, positiveCount, totalCount):
        p = float(positiveCount)/totalCount
        return  -(p*log(p) + (1-p)*log(1-p))
            
    
    def calculateEntropy(self, word):
        totalSpamDocsWithWord = self.wordCountSpam[word] # Number of spam docs which contain the word
        totalNotSpamDocsWithWord = self.wordCountNotSpam[word] # Number of non spam documents which contain the word
        totalDocsWithWord = totalSpamDocsWithWord + totalNotSpamDocsWithWord # Number of documents which contain word
        
        totalSpamDocsWithoutWord = self.totSpamDocs - totalSpamDocsWithWord # Number of spam documents which do not contain word
        totalNotSpamDocsWithoutWord = self.totNotSpamDocs - totalNotSpamDocsWithWord # Number of not spam documents which do not contain word
        totalDocsWithoutWord = totalNotSpamDocsWithoutWord + totalSpamDocsWithoutWord # Number of documents which do not contain word

        p1 = totalNotSpamDocsWithWord / totalDocsWithWord
        p2 = totalSpamDocsWithWord / totalDocsWithWord
        p3 = totalSpamDocsWithoutWord / totalDocsWithoutWord
        p4 = totalNotSpamDocsWithoutWord / totalDocsWithoutWord

        p1 = p1 * math.log(p1) if p1 != 0 else p1
        p2 = p2 * math.log(p2) if p2 != 0 else p2
        p3 = p3 * math.log(p3) if p3 != 0 else p3
        p4 = p4 * math.log(p4) if p4 != 0 else p4

        #print p1, p2, p3, p4 
        return (totalDocsWithWord / self.totTrainingDocs) * (- p1 - p2) + (totalDocsWithoutWord / self.totTrainingDocs) * (- p3 - p4)
