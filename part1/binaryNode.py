from training import TrainModel

class BinaryNode:
    def __init__(self, attribute = None, decision = None):
        self.attribute = attribute # Attribute is the chosen word
        self.decision = decision # True (is spam), False - (not spam)
        self.left = None
        self.right = None
        
    '''       
    def setAttribute(self, attribute): # Need this only for root node, which is initialized with attribute = decision = None
        self.attribute = attribute
    
    def setDecision(self, decision):
        self.decision = decision
    '''

    def insert(self, sideToInsert, attribute = None, decision = None):
        newNode = BinaryNode(attribute, decision)
        if sideToInsert == 'left':
            self.left = newNode
        elif sideToInsert == 'right':
            self.right = newNode
        else: 
            raise ValueError('need to insert binary decision node to the "left" or "right".')
        
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

