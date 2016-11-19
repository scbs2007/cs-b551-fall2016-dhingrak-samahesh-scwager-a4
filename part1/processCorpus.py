import re, os, string
from collections import Counter

'''
All file reading in this class
'''

class ProcessCorpus:
    def __init__(self, directory):
        self.directory = directory

        # Key = Word, Value = Count of the documents which contain the word
        self.wordCountInNotSpam_Bernoulli = Counter()
        self.wordCountInSpam_Bernoulli = Counter() 
        
        # Key = Word, Value = Number of occurences in training data 
        self.wordCountInNotSpam_Multinomial = Counter()
        self.wordCountInSpam_Multinomial = Counter() 

        self.allWordsInCorpus = set() 
        self.totNotSpamDocs = 0
        self.totWordsInNotSpam = 0
        self.totSpamDocs = 0
        self.totWordsInSpam = 0
        self.totTrainingDocs = 0

    def fetchTokens(self, document):
        # Currently considering words after splitting on space and removing all punctuations. all lower case.
        # TODO - Improve word check. words to use (not number, URL)
        return [str.lower(token.translate(None, string.punctuation)) for token in document.read().split()]

    # Counts w|c for both bernoulli and multinomial; total number of words in a document
    def countWordsInDocument(self, wordFreqMultinomial, wordFreqBernoulli, document):
        flag = set() # Keeps track of word that has already been counted once for a particular document - For Bernoulli Model
        count = 0 # Counts total number of words in document
        for entry in self.fetchTokens(document):
            if not self.filterWord(entry):
                count += 1
                self.allWordsInCorpus.add(entry)
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
        for fileName in os.listdir(directoryPath):
            with open(directoryPath + '/' + fileName) as document:
                wordCount += self.countWordsInDocument(wordFreqMultinomial, wordFreqBernoulli, document)
                docCount += 1
            #print "File: ", fileName
            #for entry in wordCountInDocs:
            #    print entry, wordCountInDocs[entry]
        return docCount, wordCount

    def increaseCountForWords(self, count):
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
   
    def filterWord(self, word):
        if word != '' and re.match("^[\w\d_-]*$", word):
            return False 
        return True
        
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

    def calculate(self):
        self.totNotSpamDocs, self.totWordsInNotSpam = self.creatingVector(self.wordCountInNotSpam_Multinomial, self.wordCountInNotSpam_Bernoulli, 'notspam')
        self.totSpamDocs, self.totWordsInSpam = self.creatingVector(self.wordCountInSpam_Multinomial, self.wordCountInSpam_Bernoulli, 'spam')
        # + 2 for smoothing
        self.totSpamDocs += 2
        self.totNotSpamDocs += 2
        self.totTrainingDocs = self.totNotSpamDocs + self.totSpamDocs
        
        self.smoothCounts(self.wordCountInNotSpam_Multinomial, self.wordCountInSpam_Multinomial, self.wordCountInSpam_Bernoulli, self.wordCountInNotSpam_Bernoulli)
        self.removeWordsFromConsideration()
        # TODO: Forgot to update Word Count - after removing words from consideration

    def getWordsInDocument(self, document):
        documentDict = Counter()
        for entry in self.fetchTokens(document):
            if not self.filterWord(entry):
                documentDict[entry] += 1
        return documentDict

    def getWordsInAllDocuments(self, documentDictList, classType):
        # Reading all files in train directory
        directoryPath = self.directory + '/train/' + classType
        for fileName in os.listdir(directoryPath):
            with open(directoryPath + '/' + fileName) as document:
                documentDictList.append(self.getWordsInDocument(document))


