from btTesting import TestingBinaryTree
from ntTesting import TestingNaryTree

class TestingTreeModel:
    def __init__(self, directory):
        self.directory = directory

    def testDocuments(self, modelObj):
        binary = TestingBinaryTree(modelObj, self.directory)
        binary.test()
        nary = TestingNaryTree(modelObj, self.directory)
        nary.test()
