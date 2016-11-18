from binaryTree import BinaryTree
from naryTree import NaryTree

class TrainingTreeModel:
    def __init__(self, prob):
        self.prob = prob
        self.binaryTree = None
        self.naryTree = None
    
    def train(self):
        self.binaryTree = BinaryTree(self.prob)
        self.binaryTree.train()

        self.naryTree = NaryTree(self.prob)
        self.naryTree.train()
        
        
