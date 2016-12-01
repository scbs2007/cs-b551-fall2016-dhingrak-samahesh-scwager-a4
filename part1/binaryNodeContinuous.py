
class BinaryNodeContinuous:
    def __init__(self, attribute = None, decision = None):
        self.attribute = attribute # Attribute is the chosen word
        self.decision = decision # True (is spam), False - (not spam)

        self.threshold = 0 # Value of best word at which to split
        self.left = None
        self.right = None
        
        # List of tuples (Counter - containing word:freq, class of document)
        self.leftDataAndClass = None # Documents which are to be looked into for finding the left successor
        self.rightDataAndClass = None # Documents which are to be looked into for finding the right successor
        
        # Set containing words out of consideration for entropy calculation for the next iteration
        self.ignoreWords = set() 

    def setAttribute(self, attribute): # Need this only for root node, which is initialized with attribute = decision = None
        self.attribute = attribute
    
    def setDecision(self, decision):
        self.decision = decision
    
    def setIgnoreWords(self, wordList):
        self.ignoreWords = wordList

    def setThreshold(self, thresh):
        self.threshold = thresh

    def setLeftAndRightData(self, data):
        self.leftDataAndClass, self.rightDataAndClass = data
