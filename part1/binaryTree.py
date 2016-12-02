# Implemented ID3 Algorithm

from __future__ import division
import math, itertools, sys
from binaryNode import BinaryNode
#from multiprocessing.pool import Pool as ThreadPool

class BinaryTree:
    def __init__(self, processCorpus, spamDocuments, notSpamDocuments):
        self.processCorpus = processCorpus
        self.root = None
        self.wordCountNotSpam = processCorpus.wordCountInNotSpam_Bernoulli 
        self.wordCountSpam = processCorpus.wordCountInSpam_Bernoulli
        self.totTrainingDocs = processCorpus.totTrainingDocs 
        self.totSpamDocs = processCorpus.totSpamDocs
        self.totNotSpamDocs = processCorpus.totNotSpamDocs
        self.allWords = list(processCorpus.allWordsInCorpus) #list with all the words in all emails
        '''
        each list element contains a counter dict for each word in a given document.
        for bernoulli, simply check whether word is in the counter dict. for multinomial, look at the word's value
        '''
        self.documentDictListSpam = spamDocuments 
        self.documentDictListNotSpam = notSpamDocuments

    def dtLearning(self):
        print "Training Decision Tree Model - binary values (ID3 Algorithm)... Please wait..."
        #pool = ThreadPool(10) # Thread pool 
        rootWord = self.mostImportantWordForRoot() # Split on this word #print rootWord
        root = BinaryNode(attribute=rootWord)
        root.setIgnoreWords(set([rootWord]))
        root.setSpamDocsIndexes(*self.createDocsIndexListForRoot(self.documentDictListSpam, rootWord))
        root.setNotSpamDocsIndexes(*self.createDocsIndexListForRoot(self.documentDictListNotSpam, rootWord))
        maxTreeHeight = 20 # Height uptil which tree is to be built - Found this value via 5 fold cross validation.
        self.buildTree(root, maxTreeHeight)
        self.root = root
        
        #pool.close()
        #pool.join()

    def createDocsIndexListForRoot(self, documents, attribute):
        withWord = []
        withoutWord = []
        for index in range(len(documents)):
            if attribute in documents[index]:
                withWord.append(index)
            else:
                withoutWord.append(index)
        return [withWord, withoutWord]
    
    def createDocsIndexListForNode(self, documentIndexes, documents, attribute):
        withWord = []
        withoutWord = []
        for index in documentIndexes:
            if attribute in documents[index]:
                withWord.append(index)
            else:
                withoutWord.append(index)
        #if len(withWord) == 0 and len(withoutWord) == 0:
        #    return [[], []]
        return [withWord, withoutWord]
    
    def buildTree(self, node, height):
        #print "Current Node: ", node.attribute
        #sys.exit(0)
       
        if height == 0:
            self.setDecision(node)
            return
        
        # No subset of records found
        if self.checkNoSubset(node.indexSpamDocsWithWord, node.indexSpamDocsWithoutWord, node.indexNotSpamDocsWithWord, node.indexNotSpamDocsWithoutWord): 
            #print "No subset found"
            self.setDecision(node)
            return 
        
        # If there are no more words to split on
        if self.checkAllWordsUsed(node.ignoreWords):
            #print "No More words to split on"
            self.setDecision(node)
            return

        # For Left Branch
        sameClass = self.checkIfSameClassLeft(node)
        if sameClass[0] == True:
        # Do the records belong to the same class? No need to build the tree further
            #print "All records in this node belong to the same class: ", sameClass[1]
            leafNode = BinaryNode(decision=sameClass[1])
            self.insert(node, 'left', leafNode)
        else:
            leftWord = self.findBestSplitNode(node, 'left') 
            self.insert(node, 'left', leftWord)
            self.buildTree(node.left, height - 1)

        #print "Current Node: ", node.attribute
        # For Right Branch
        sameClass = self.checkIfSameClassRight(node)
        if sameClass[0] == True:
        # Do the records belong to the same class? No need to build the tree further
            #print "All records in this node belong to the same class: ", sameClass[1]
            leafNode = BinaryNode(decision=sameClass[1])
            self.insert(node, 'right', leafNode)
            return
        else:
            rightWord = self.findBestSplitNode(node, 'right') 
            self.insert(node, 'right', rightWord)
            self.buildTree(node.right, height - 1)
       
    def findBestSplitNode(self, node, branch):
        # Find words which are to be considered for entropy calculation
        wordList = self.wordsToConsider(node)
        numberOfWords = len(wordList)
        
        # Entropy Calculation
        if branch == 'left':
            entropies = map(self.findWordEntropy, zip(                                                                                   \
                                                        wordList,                                                                        \
                                                        list(itertools.repeat(node.indexSpamDocsWithoutWord, numberOfWords)),            \
                                                        list(itertools.repeat(node.indexNotSpamDocsWithoutWord, numberOfWords))))
            #print "Left: ", wordList[entropies.index(min(entropies))]
            '''co = 0
            for i in wordList:
                #print i, ": ", entropies[co]
                co +=1
            sys.exit(0)
            '''
        else:
            entropies = map(self.findWordEntropy, zip(                                                                                   \
                                                        wordList,                                                                        \
                                                        list(itertools.repeat(node.indexSpamDocsWithWord, numberOfWords)),               \
                                                        list(itertools.repeat(node.indexNotSpamDocsWithWord, numberOfWords))))
            #print "Right: ", wordList[entropies.index(min(entropies))]
        #print "Entropy: ", min(entropies) 
        bestWord = wordList[entropies.index(min(entropies))]
        newNode = BinaryNode(attribute=bestWord)
        newNode.setIgnoreWords(set([bestWord])|node.ignoreWords)
        #print "Words to ignore while entropy calculation: ", sorted(newNode.ignoreWords)
             
        if branch == 'left':
            indexSpamDocsWithWord, indexSpamDocsWithoutWord = self.createDocsIndexListForNode(node.indexSpamDocsWithoutWord, self.documentDictListSpam, bestWord)
            indexNotSpamDocsWithWord, indexNotSpamDocsWithoutWord = self.createDocsIndexListForNode(node.indexNotSpamDocsWithoutWord, \
                                                                                                    self.documentDictListNotSpam, bestWord)
        else:
            indexSpamDocsWithWord, indexSpamDocsWithoutWord = self.createDocsIndexListForNode(node.indexSpamDocsWithWord, self.documentDictListSpam, bestWord)
            indexNotSpamDocsWithWord, indexNotSpamDocsWithoutWord = self.createDocsIndexListForNode(node.indexNotSpamDocsWithWord, \
                                                                                                    self.documentDictListNotSpam, bestWord)
        newNode.setSpamDocsIndexes(indexSpamDocsWithWord, indexSpamDocsWithoutWord)
        newNode.setNotSpamDocsIndexes(indexNotSpamDocsWithWord, indexNotSpamDocsWithoutWord)
        
        return newNode
       
    def checkIfSameClassLeft(self, node):
        # Returns - (Same Class?, What's the class)
        if len(node.indexSpamDocsWithoutWord) == 0 and len(node.indexNotSpamDocsWithoutWord) != 0:
            return (True, False)    # Not Spam
        elif len(node.indexSpamDocsWithoutWord) != 0 and len(node.indexNotSpamDocsWithoutWord) == 0:
            return (True, True)     # Spam
        return (False, None)
    
    def checkIfSameClassRight(self, node):
        # Returns - (Same Class?, What's the class)
        if len(node.indexSpamDocsWithWord) == 0 and len(node.indexNotSpamDocsWithWord) != 0:
            return (True, False)
        elif len(node.indexSpamDocsWithWord) != 0 and len(node.indexNotSpamDocsWithWord) == 0:
            return (True, True)
        return (False, None)
 
    def checkAllWordsUsed(self, words):
        if len(words) == len(self.allWords): # If there are no more words to split on
            return True
        return False
    
    def checkNoSubset(self, indexSpamDocsWithWord, indexSpamDocsWithoutWord, indexNotSpamDocsWithWord, indexNotSpamDocsWithoutWord):
        # No subset of records found
        if (indexSpamDocsWithWord == [] and indexNotSpamDocsWithWord == []) or (indexSpamDocsWithoutWord == [] and indexNotSpamDocsWithoutWord == []):
            return True
        return False
 
    def setDecision(self, node, decision = None):
        if decision == None:
            # Set decision for parent to class having higher count
            node.setDecision(self.findClassWithHigherCount(node.indexSpamDocsWithoutWord, node.indexNotSpamDocsWithoutWord, \
                                                           node.indexSpamDocsWithWord, node.indexNotSpamDocsWithWord))
        else:
            node.setDecision(decision)
    
    # Finds Class having higher count
    def findClassWithHigherCount(self, spamWithout, notSpamDocsWithout, spamDocsWith, notSpamDocsWith):
        spamCount = len(spamWithout) + len(spamDocsWith)
        notSpamCount = len(notSpamDocsWithout) + len(notSpamDocsWith)
        if spamCount > notSpamCount:
            return True
        else:
            return False

    # Returns list of words to be considered for entropy calculation  
    def wordsToConsider(self, node):
        return [word for word in self.allWords if word not in node.ignoreWords]
 
    def insert(self, node, sideToInsert, newNode):
        if sideToInsert == 'left':
            node.left = newNode
        elif sideToInsert == 'right':
            node.right = newNode
        '''
        else: 
            raise ValueError('need to insert binary decision node to the "left" or "right".')
        '''

    def findWordEntropy(self, argument):
        word, indexSpamDocs, indexNotSpamDocs = argument
        #print "Entopry calculation for: ", word
        #print "Spam docs indexes: ", indexSpamDocs
        #print "Non Spam Docs indexes: ", indexNotSpamDocs
        positiveCountSpam = 0
        negativeCountSpam = 0
        positiveCountNotSpam = 0
        negativeCountNotSpam = 0
        
        for index in indexNotSpamDocs: 
            if word in self.documentDictListNotSpam[index]: 
                positiveCountNotSpam += 1
            else: 
                negativeCountNotSpam += 1
            
        for index in indexSpamDocs: 
            if word in self.documentDictListSpam[index]: 
                positiveCountSpam += 1
            else: 
                negativeCountSpam += 1

        # This word was not present in any of the partitions
        if positiveCountSpam == 0 and negativeCountSpam == 0 and positiveCountNotSpam == 0 and negativeCountNotSpam == 0:
            return sys.maxint
        return self.entropyHelper(positiveCountSpam, negativeCountSpam, positiveCountNotSpam, negativeCountNotSpam) 

    def entropyHelper(self, positiveCountSpam, negativeCountSpam, positiveCountNotSpam, negativeCountNotSpam):
        totSpam = positiveCountSpam + negativeCountSpam
        totNotspam = positiveCountNotSpam + negativeCountNotSpam
        tot = totSpam + totNotspam
        totPositiveCount = positiveCountNotSpam + positiveCountSpam
        totNegativeCount = negativeCountSpam + negativeCountNotSpam
        #print "in not spam: ", positiveCountNotSpam, "in spam: ", positiveCountSpam
        p1 = self.checkLog(positiveCountNotSpam, totPositiveCount)
        p2 = self.checkLog(positiveCountSpam, totPositiveCount)
        
        p3 = self.checkLog(negativeCountSpam, totNegativeCount)
        p4 = self.checkLog(negativeCountNotSpam, totNegativeCount)

        #print p1, p2, p3, p4
        return ((positiveCountSpam + positiveCountNotSpam) / tot) * (- p1 - p2) + ((negativeCountSpam + negativeCountNotSpam) / tot) * (- p3 - p4)
 
    def mostImportantWordForRoot(self):
        #print "Consider words: ", self.allWords
        entropies = map(self.calculateEntropyForRoot, self.allWords)
        '''for i in range(len(self.allWords)):
            if entropies[i] < 0.6:
                print self.allWords[i], entropies[i]
        '''
        #print "Min Entropy Root: ", min(entropies)
        #sys.exit(0)
        
        return self.allWords[entropies.index(min(entropies))]
    
    def checkLog(self, value1, value2):
        if value1 == 0:
            return 0
        prob = value1/value2
        return prob * math.log10(prob)
    
    # TODO: Remove this - use the other functino for root also. 
    def calculateEntropyForRoot(self, word):
        totalSpamDocsWithWord = self.wordCountSpam[word] # Number of spam docs which contain the word
        totalNotSpamDocsWithWord = self.wordCountNotSpam[word] # Number of non spam documents which contain the word
        totalDocsWithWord = totalSpamDocsWithWord + totalNotSpamDocsWithWord # Number of documents which contain word
        
        totalSpamDocsWithoutWord = self.totSpamDocs - totalSpamDocsWithWord # Number of spam documents which do not contain word
        totalNotSpamDocsWithoutWord = self.totNotSpamDocs - totalNotSpamDocsWithWord # Number of not spam documents which do not contain word
        totalDocsWithoutWord = totalNotSpamDocsWithoutWord + totalSpamDocsWithoutWord # Number of documents which do not contain word
        '''if word == "affiliates":
            print "Total Spam with: ", totalSpamDocsWithWord
            print "Total Not Spam with: ", totalNotSpamDocsWithWord
            print "Total Spam without: ", totalSpamDocsWithoutWord
            print "Total Not Spam without: ", totalNotSpamDocsWithoutWord
        '''    
        p1 = self.checkLog(totalNotSpamDocsWithWord, totalDocsWithWord)
        p2 = self.checkLog(totalSpamDocsWithWord, totalDocsWithWord)
        
        p3 = self.checkLog(totalSpamDocsWithoutWord, totalDocsWithoutWord)
        p4 = self.checkLog(totalNotSpamDocsWithoutWord, totalDocsWithoutWord)

        #print p1, p2, p3, p4
        return (totalDocsWithWord / self.totTrainingDocs) * (- p1 - p2) + (totalDocsWithoutWord / self.totTrainingDocs) * (- p3 - p4)
   
    def display(self, depth = 0):
        print "depth: ", depth
        if self.attribute:
            print "word: ", self.attribute
        if self.decision:
            print "decision node: ", "is spam" if self.decision is True else "is not spam"
        if self.left:
            print "if '" + self.attribute + "' is not in document:"
            self.left.display(depth = depth + 1)
        if self.right:
            print "if '" + self.attribute + "' is in document:"
            self.right.display(depth = depth + 1)
