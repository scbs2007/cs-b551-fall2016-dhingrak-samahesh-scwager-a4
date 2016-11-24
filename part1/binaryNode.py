from training import TrainModel

class BinaryNode:
    def __init__(self, attribute = None, decision = None):
        self.attribute = attribute # Attribute is the chosen word
        self.decision = decision # True (is spam), False - (not spam)
        self.left = None
        self.right = None

        self.indexSpamDocsWithWord = [] # Contains the indexes of the docs in documentDictListSpam which are to be looked into for finding right successor
        self.indexNotSpamDocsWithWord = [] # Contains the indexes of the docs in documentDictListNotSpam which are to be looked into for finding right successor

        self.indexSpamDocsWithoutWord = [] # Contains the indexes of the docs in documentDictListSpam which are to be looked into for finding left successor
        self.indexNotSpamDocsWithoutWord = [] # Contains the indexes of the docs in documentDictListNotSpam which are to be looked into for finding left successor

        self.ignoreWords = set() # Set containing words out of consideration for entropy calculation for the next iteration
        
    def setAttribute(self, attribute): # Need this only for root node, which is initialized with attribute = decision = None
        self.attribute = attribute
    
    def setDecision(self, decision):
        self.decision = decision
    
    def setIgnoreWords(self, wordList):
        self.ignoreWords = wordList

    def setSpamDocsIndexes(self, withWord, withoutWord):  
	#print withWord, withoutWord
        self.indexSpamDocsWithWord = withWord
        self.indexSpamDocsWithoutWord = withoutWord
    
    def setNotSpamDocsIndexes(self, withWord, withoutWord):  
	#print withWord, withoutWord
        self.indexNotSpamDocsWithWord = withWord
        self.indexNotSpamDocsWithoutWord = withoutWord

