from __future__ import division
import os, string, sys, math, pickle, re
from collections import Counter

from binaryTree import BinaryTree
from binaryTreeContinuous import BinaryTreeContinuous
from processCorpus import ProcessCorpus

class TrainingTreeModel:
    def __init__(self, directory):
        self.directory = directory
        self.processCorpus = ProcessCorpus(directory)
        self.binaryTree = None
        self.btc = None
        '''
        each list element contains a counter dict for each word in a given document.
        for bernoulli, simply check whether word is in the counter dict. for multinomial, look at the word's value
        '''
        self.documentDictListSpam = []
        self.documentDictListNotSpam = []
        
    def train(self):
        print "Total time that will be taken is around 8.73 minutes."
        self.processCorpus.calculate('tree')
        self.processCorpus.getWordsInAllDocuments(self.documentDictListSpam, 'spam')
        self.processCorpus.getWordsInAllDocuments(self.documentDictListNotSpam, 'notspam')

        self.binaryTree = BinaryTree(self.processCorpus, self.documentDictListSpam, self.documentDictListNotSpam)
        self.binaryTree.dtLearning()

        self.btc = BinaryTreeContinuous(self.processCorpus, self.documentDictListSpam, self.documentDictListNotSpam)
        self.btc.dtLearning()
