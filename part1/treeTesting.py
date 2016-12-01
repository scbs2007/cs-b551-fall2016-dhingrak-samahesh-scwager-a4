from btTesting import TestingBinaryTree
from btContinuousTesting import TestingBinaryTreeContinuous

class TestingTreeModel:
    def __init__(self, directory):
        self.directory = directory

    def testDocuments(self, modelObj):
        binary = TestingBinaryTree(modelObj, self.directory)
        binary.test()
        btc = TestingBinaryTreeContinuous(modelObj, self.directory)
        btc.test()
