from binaryNode import BinaryNode

class BinaryTree:
    def __init__(self, probabilities, spamDocuments, notSpamDocuments):
        self.prob = probabilities
        self.root = None
        self.wordCountNotSpam = self.prob.wordCountInNotSpam_Bernoulli 
        self.wordCountSpam = self.prob.wordCountInSpam_Bernoulli
        self.wordList = list( set( self.wordCountNotSpam.keys() + self.wordCountSpam.keys() ) ) #list with all the words in all emails
        '''
        each list element contains a counter dict for each word in a given document.
        for bernoulli, simply check whether word is in the counter dict. for multinomial, look at the word's value
        '''
        self.documentDictListSpam = spamDocuments 
        self.documentDictListNotSpam = notSpamDocuments

    def train(self):
        self.decisionTreeLearning_Bernoulli()

    def decisionTreeLearning_Bernoulli(self, maxHeight = 1):
        rootWord = self.mostImportantWord()
        self.root = BinaryNode(attribute = rootWord)
        
        #print self.documentDictListSpam[0]
        
        leftCondition = {rootWord: 0}
        rightCondition = {rootWord: 1}
        return self.root

    def decisionTreeLearningHelp_Bernoulli(self, condition, remainingHeight):
        return

    def mostImportantWord(self, condition = {}): 
        bestWord, entropy = "", 1.1
        for w in self.wordList:
            positiveCountSpam = negativeCountSpam = positiveCountNotSpam = negativeCountNotSpam = 0
            '''
            do to: add statement: if condition holds (e.g. word1 is not in document, word2 is in document, word3, ...etc)
            so that only the words that are on this branch are counted
            documentDictListSpam: each list element contains a counter dict for each word in a given document.
            for bernoulli, simply check whether word is in the counter dict. for multinomial, look at the word's value
            '''
            if w in self.documentDictListNotSpam: positiveCountNotSpam += 1
            else: negativeCountNotSpam += 1
            if w in self.documentDictListSpam: positiveCountSpam += 1
            else: negativeCountSpam += 1
            
            '''
            next, calculate entropy in the left and right branches. replace bestWord and entropy if the current value is 
            better
            '''
        pass
            
            
    def entropy_Bernoulli(self, positiveCount, totalCount):
        p = float(positiveCount)/totalCount
        return  -(p*log(p) + (1-p)*log(1-p))
            
        
 
