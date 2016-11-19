from __future__ import division
import os, string, sys, math, pickle
from collections import Counter
import re

from binaryTree import BinaryTree
from naryTree import NaryTree

class TrainingTreeModel:
    def __init__(self, directory, prob):
        self.prob = prob
        self.binaryTree = None
        self.naryTree = None
        self.documentDictListSpam = []
        self.documentDictListNotSpam = []
        self.directory = directory
        
    def fetchTokens(self, document):
        # Currently considering words after splitting on space and removing all punctuations. all lower case.
        # TODO - Improve word check. words to use (not number, URL)
        return [str.lower(token.translate(None, string.punctuation)) for token in document.read().split()]
        
    def train(self):
        
        self.getWordsInAllDocuments(self.documentDictListSpam, 'spam')
        self.getWordsInAllDocuments(self.documentDictListNotSpam, 'notspam')

        self.binaryTree = BinaryTree(self.prob, self.documentDictListSpam, self.documentDictListNotSpam)
        self.binaryTree.train()

        self.naryTree = NaryTree(self.prob)
        self.naryTree.train()

    def getWordsInDocument(self, document):
        flag = set() # Keeps track of word that has already been counted once for a particular document - For Bernoulli Model
        count = 0 # Counts total number of words in document
        documentDict = Counter()
        for entry in self.fetchTokens(document):
            if entry != '' and re.match("^[\w\d_-]*$", entry):
                documentDict[entry] += 1
#         for entry in  documentDict:
#             print entry,  documentDict[entry]
#         quit()
        return documentDict

    def getWordsInAllDocuments(self, documentDictList, classType):
        # Reading all files in train directory
        directoryPath = self.directory + '/train/' + classType
        for fileName in os.listdir(directoryPath):
            with open(directoryPath + '/' + fileName) as document:
                documentDictList.append( self.getWordsInDocument(document) )

        
