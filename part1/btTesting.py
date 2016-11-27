import os
from collections import deque

class TestingBinaryTree:
    def __init__(self, trainedModel, directory):
        self.modelObj = trainedModel
        self.directory = directory
        # True Positive, False Negative, False Positive, True Negative
        self.confidenceMatrix = [0, 0, 0, 0]

    def displayAccuracy(self):
        print "\n\nAccuracy Percentage: ", round((self.confidenceMatrix[0] + self.confidenceMatrix[3]) * 100.0 / sum(self.confidenceMatrix), 2)
        print "Confidence Matrix: "
        print "True Positive: ", self.confidenceMatrix[0]
        print "False Negative: ", self.confidenceMatrix[1] 
        print "False Positive: ", self.confidenceMatrix[2] 
        print "True Negative: ", self.confidenceMatrix[3] 
    
    def updateConfidenceMatrix(self, classType, result):
        if classType == 'spam':
            if result == classType:
                self.confidenceMatrix[0] += 1
            else:
                self.confidenceMatrix[2] += 1
        elif classType == 'notspam':
            if result == classType:
                self.confidenceMatrix[3] += 1
            else:
                self.confidenceMatrix[1] += 1

    def testOnTree(self, words, root):
        if root.decision == None:
            if root.attribute in words:
                return self.testOnTree(words, root.right)
            else:
                return self.testOnTree(words, root.left)

        return 'spam' if root.decision == True else 'notspam'

    def testDocuments(self, classType):
        directoryPath = self.directory + '/test/' + classType
        for fileName in os.listdir(directoryPath):
            with open(directoryPath + '/' + fileName) as document:
                wordList = self.modelObj.processCorpus.fetchTokens(document)
                root = self.modelObj.binaryTree.root
                result = self.testOnTree(wordList, root)
                self.updateConfidenceMatrix(classType, result)

    def displayFour(self):
        root = self.modelObj.binaryTree.root
        q = deque([root])
        q.append('#')
        count = 0
        result = [[], [], [], []]
        result[0] = [root.attribute]
        while count < 3 and q:
            node = q.popleft()
            while node != '#':
                if node.left != None:
                    q.append(node.left)
                    result[count + 1].append(node.left.attribute)
                
                if node.right != None:
                    q.append(node.right)
                    result[count + 1].append(node.right.attribute)
                node = q.popleft()
            q.append('#') 
            count += 1
        print "\n\nTop 4 layers of the tree: (Left branch - Word was absent. Right branch - Word was present.)"
        iteration = 1
        for entry in result:
            print "Layer ", iteration, ": ", entry    
            iteration += 1
            
    def test(self):
        print "Testing On Binary Tree!"
        self.testDocuments('spam')
        self.testDocuments('notspam')
        self.displayAccuracy()
        self.displayFour()
