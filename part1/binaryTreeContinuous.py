# Implemented c4.5 Algorithm for training Decision Tree considering continuous attribute value.

from __future__ import division
from binaryNodeContinuous import BinaryNodeContinuous
from operator import itemgetter
import itertools, math

class BinaryTreeContinuous:
    def __init__(self, processCorpus, spamDocuments, notSpamDocuments):
        self.processCorpus = processCorpus
        self.spamDocs = spamDocuments # List of Counter objects
        self.notSpamDocs = notSpamDocuments # List of Counter objects
        self.allWords = processCorpus.allWordsInCorpus # set containing all the words in all docs
        self.root = None

    # Returns a list of tuples - (Counter obj, Class). True = spam; False = not spam
    def combineCorpus(self):
        # Combining the corpus will make things easy. Can optimize later if need be.
        return [(entry, True) for entry in self.spamDocs] + [(entry, False) for entry in self.notSpamDocs]

    def getWordsToConsider(self, toIgnore):
        return self.allWords - toIgnore

    def checkAllWordsUsed(self, words):
        if words == self.allWords: # If there are no more words to split on
            return True
        return False
    
    def checkNoSubset(self, node):
        # No subset of records found
        return True if node.leftDataAndClass == [] or node.rightDataAndClass == [] else False
 
    def setDecision(self, node, decision = None):
        if decision == None:
            # Set decision for parent to class having higher count
            node.setDecision(self.findClassWithHigherCount(node))
            #print "In set decision if. Decision: ", node.decision
            #sys.exit(0)
        else:
            #print "In set decision else. Decision: ", node.decision
            node.setDecision(decision)
   
    def findCountOfClassInData(self, data):
        spamCount = 0
        notSpamCount = 0
        for entry in data:
            if entry[1]:
                spamCount += 1
            else:
                notSpamCount += 1
        return spamCount, notSpamCount
 
    # Finds Class having higher count
    def findClassWithHigherCount(self, node):
        dataAndClassLeft = node.leftDataAndClass
        dataAndClassRight = node.rightDataAndClass

        spamCount, notSpamCount = self.findCountOfClassInData(dataAndClassLeft)
        #print "spam count, not spam count: ", spamCount, notSpamCount
        counts = self.findCountOfClassInData(dataAndClassRight)
        spamCount += counts[0]
        notSpamCount += counts[1]
        #print "spam count, not spam count: ", spamCount, notSpamCount
        return True if spamCount > notSpamCount else False
    
    def findRootWord(self, allDataAndClass):
        words = list(self.allWords)
        entropiesAndThresh = map(self.getEntropyAndThresh, zip(self.allWords, itertools.repeat(allDataAndClass, len(words))))
        minEntropyAndThresh = min(entropiesAndThresh, key=itemgetter(0))
        minIndex = entropiesAndThresh.index(minEntropyAndThresh)
        '''print "Entropies and thresh: ", entropiesAndThresh
        print "Index: ", minIndex
        print "Min Entropy and thresh: ", entropiesAndThresh[minIndex]
        print "word: ", words[minIndex]
        '''
        return words[minIndex], minEntropyAndThresh[1] # Return word and the value of freq for this word at which min entropy was found

    def findLeftAndRightData(self, allDataAndClass, threshold, bestSplitWord):
        leftDataAndClass = []
        rightDataAndClass = []
        for entry in allDataAndClass:
            if entry[0][bestSplitWord] <= threshold:
                leftDataAndClass.append(entry)
            else:
                rightDataAndClass.append(entry)
        return [leftDataAndClass, rightDataAndClass]

    def checkIfSameClass(self, data):
        # Returns - (Same Class?, What's the class)
        spamCount, notSpamCount = self.findCountOfClassInData(data)
        if spamCount == 0 and notSpamCount != 0:
            return (True, False)    # Not Spam
        elif spamCount != 0 and notSpamCount == 0:
            return (True, True)     # Spam
        else:
            return (False, None)
    
    def dtLearning(self):
        print "Training Decision Tree Model for continuous values... Please wait..."
        height = 19 # Height uptil which to build the tree - Found via 5 fold cross validation
        root = BinaryNodeContinuous()
        allDataAndClass = self.combineCorpus()
        bestSplitWord, threshold = self.findRootWord(allDataAndClass) # Split on this word 
        root.setAttribute(bestSplitWord)
        root.setIgnoreWords(set([bestSplitWord]))
        root.setThreshold(threshold)
        root.setLeftAndRightData(self.findLeftAndRightData(allDataAndClass, threshold, bestSplitWord))
        #print bestSplitWord, threshold
        #print root.leftDataAndClass[0][0]#['jalapeno'], 
        #print root.rightDataAndClass[0][0]#['jalapeno'] 
        #sys.exit(0)
        self.buildTree(root, height)
        self.root = root

    def buildTree(self, node, height):
        #print "Current Node: ", node.attribute
        if height == 0:
            #print "Height 0"
            self.setDecision(node)
            return

        # No subset of records found
        if self.checkNoSubset(node): 
            #print "No subset found"
            self.setDecision(node)
            return 
        
        # If there are no more words to split on
        if self.checkAllWordsUsed(node.ignoreWords):
            #print "No More words to split on"
            self.setDecision(node)
            return

        # For Left Branch
        sameClass = self.checkIfSameClass(node.leftDataAndClass)
        if sameClass[0] == True:
        # Do the records belong to the same class? No need to build the tree further
            #print "All records in this node belong to the same class: ", sameClass[1]
            leafNode = BinaryNodeContinuous(decision=sameClass[1])
            self.insert(node, 'left', leafNode)
            #print "Leaf: ", leafNode.decision
        else:
            leftWord = self.findBestSplitNode(node, 'left') 
            self.insert(node, 'left', leftWord)
            self.buildTree(node.left, height - 1)

        #print "Current Node: ", node.attribute
        # For Right Branch
        sameClass = self.checkIfSameClass(node.rightDataAndClass)
        if sameClass[0] == True:
        # Do the records belong to the same class? No need to build the tree further
            #print "All records in this node belong to the same class: ", sameClass[1]
            leafNode = BinaryNodeContinuous(decision=sameClass[1])
            self.insert(node, 'right', leafNode)
            #print "Leaf: ", leafNode.decision
            return
        else:
            rightWord = self.findBestSplitNode(node, 'right') 
            self.insert(node, 'right', rightWord)
            self.buildTree(node.right, height - 1)

    def findBestSplitNode(self, node, branch):
        # Find words which are to be considered for entropy calculation
        wordList = list(self.getWordsToConsider(node.ignoreWords))
        numberOfWords = len(wordList)

        #if node.attribute  == 'yellow':
        '''print node.attribute, node.threshold
        print "Left: "
        for entry in node.leftDataAndClass:
            print entry[0][node.attribute], 
        print "Right: "
        for entry in node.rightDataAndClass:
            print entry[0][node.attribute],
        sys.exit(0)
        '''

        # Entropy Calculation
        if branch == 'left':
            entropiesAndThresh = map(self.getEntropyAndThresh, zip(wordList, itertools.repeat(node.leftDataAndClass, numberOfWords)))
            minEntropyAndThresh = min(entropiesAndThresh, key=itemgetter(0))
            minIndex = entropiesAndThresh.index(minEntropyAndThresh)
            #print "Left: ", wordList[minIndex]
            #return words[minIndex], minEntropyAndThresh[1] # Return word and the value of freq for this word at which min entropy was found
        else:
            entropiesAndThresh = map(self.getEntropyAndThresh, zip(wordList, itertools.repeat(node.rightDataAndClass, numberOfWords)))
            minEntropyAndThresh = min(entropiesAndThresh, key=itemgetter(0))
            minIndex = entropiesAndThresh.index(minEntropyAndThresh)
            #return words[minIndex], minEntropyAndThresh[1] # Return word and the value of freq for this word at which min entropy was found
            #print "Right: ", wordList[minIndex]
        '''print "Entropies and thresh: ", entropiesAndThresh
        print "Index: ", minIndex
        print "Min Entropy and thresh: ", entropiesAndThresh[minIndex]
        print "word: ", words[minIndex]
        '''
 
        #print "Entropy: ", min(entropies) 
        bestWord = wordList[minIndex]
        newNode = BinaryNodeContinuous(attribute=bestWord)
        newNode.setIgnoreWords(set([bestWord])|node.ignoreWords)
        threshold = minEntropyAndThresh[1]
        newNode.setThreshold(threshold)
        #print "Words to ignore while entropy calculation: ", sorted(newNode.ignoreWords)
        if branch == 'left':
            newNode.setLeftAndRightData(self.findLeftAndRightData(node.leftDataAndClass, threshold, bestWord))
        else:
            newNode.setLeftAndRightData(self.findLeftAndRightData(node.rightDataAndClass, threshold, bestWord))
        return newNode

    # Returns tuple - (the word at which to split, threshold value of this word)
    def getEntropyAndThresh(self, argument):
        word, counterAndClass = argument
        counterClassWithFreq, freqValues = self.fetchDataAndFrequency(counterAndClass, word)
        numberOfValues = len(freqValues)
        
        # Entropies for splits at all unique frequencies of the word
        entropies = map(self.calculateEntropy, zip(itertools.repeat(counterClassWithFreq, numberOfValues), freqValues))
        minIndex = entropies.index(min(entropies))
        '''if word == 'jalapeno':
            print "Entropies: ", entropies
            print "Index: ", minIndex
            print "Min Entropy: ", entropies[minIndex]
            print "Min Freq: ", list(freqValues)[minIndex]
        '''
        '''print "Entropies: ", entropies
        print "Index: ", minIndex
        print "Min Entropy: ", entropies[minIndex]
        print "Min Freq: ", list(freqValues)[minIndex]
        sys.exit(0)'''
        return entropies[minIndex], freqValues[minIndex] # Return min entropy and the value of freq of word at which this min entropy was obtained
       
    def calculateEntropy(self, argument): 
        counterClassWithFreq, thresh = argument
        #print "Thresh: ", thresh 
        
        positiveCountSpam = 0
        positiveCountNotSpam = 0
        negativeCountSpam = 0
        negativeCountNotSpam = 0
        for (_, classType), freq in counterClassWithFreq:
            if freq <= thresh:
                if classType: # True - Spam
                    positiveCountSpam += 1
                else:
                    positiveCountNotSpam += 1
            else:
                if classType:
                    negativeCountSpam += 1
                else:
                    negativeCountNotSpam += 1
        #print "Entropy: ", self.entropyHelper(positiveCountSpam, negativeCountSpam, positiveCountNotSpam, negativeCountNotSpam)
        return self.entropyHelper(positiveCountSpam, negativeCountSpam, positiveCountNotSpam, negativeCountNotSpam)
                
    # Returns sorted list - [((Counter, class), frequency of word)] and list - all Frequencies for word
    def fetchDataAndFrequency(self, counterWithClass, word):
        counterClassWithFreq = []
        allFreq = set([])
        
        for eachDoc in counterWithClass:
            freq = eachDoc[0][word]
            counterClassWithFreq.append((eachDoc, freq))
            allFreq.add(freq)
        return sorted(counterClassWithFreq, key=itemgetter(1)), list(allFreq)

    def entropyHelper(self, positiveCountSpam, negativeCountSpam, positiveCountNotSpam, negativeCountNotSpam):
        totSpam = positiveCountSpam + negativeCountSpam
        totNotspam = positiveCountNotSpam + negativeCountNotSpam
        tot = totSpam + totNotspam
        totPositiveCount = positiveCountNotSpam + positiveCountSpam
        totNegativeCount = negativeCountSpam + negativeCountNotSpam
        
        p1 = self.checkLog(positiveCountNotSpam, totPositiveCount)
        p2 = self.checkLog(positiveCountSpam, totPositiveCount)
        
        p3 = self.checkLog(negativeCountSpam, totNegativeCount)
        p4 = self.checkLog(negativeCountNotSpam, totNegativeCount)

        return ((positiveCountSpam + positiveCountNotSpam) / tot) * (- p1 - p2) + ((negativeCountSpam + negativeCountNotSpam) / tot) * (- p3 - p4)

    def checkLog(self, value1, value2):
        if value1 == 0:
            return 0
        prob = value1/value2
        return prob * math.log10(prob)
       
    def insert(self, node, sideToInsert, newNode):
        if sideToInsert == 'left':
            node.left = newNode
        elif sideToInsert == 'right':
            node.right = newNode
