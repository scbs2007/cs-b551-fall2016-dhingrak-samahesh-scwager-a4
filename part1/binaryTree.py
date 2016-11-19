from binaryNode import BinaryNode

class BinaryTree:
    def __init__(self, processCorpus, spamDocuments, notSpamDocuments):
        self.processCorpus = processCorpus
        self.root = None
        self.wordCountNotSpam = self.processCorpus.wordCountInNotSpam_Bernoulli 
        self.wordCountSpam = self.processCorpus.wordCountInSpam_Bernoulli
        self.wordList = self.processCorpus.allWordsInCorpus #list with all the words in all emails
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
        pass
            
    def entropy_Bernoulli(self, positiveCount, totalCount):
        p = float(positiveCount)/totalCount
        return  -(p*log(p) + (1-p)*log(1-p))
            
        
 
