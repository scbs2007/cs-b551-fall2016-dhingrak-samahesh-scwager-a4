import os
from collections import deque

class TestingBinaryTreeContinuous:
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

    def testOnTree(self, wordCounter, root):
        if root.decision == None:
            if wordCounter[root.attribute] <= root.threshold:
                return self.testOnTree(wordCounter, root.left)
            else:
                return self.testOnTree(wordCounter, root.right)
        return 'spam' if root.decision == True else 'notspam'

    def testDocuments(self, classType):
        directoryPath = self.directory + '/test/' + classType
        for fileName in os.listdir(directoryPath):
            with open(directoryPath + '/' + fileName) as document:
                wordCounter = self.modelObj.processCorpus.getWordsInDocument(document)
                root = self.modelObj.btc.root
                result = self.testOnTree(wordCounter, root)
                self.updateConfidenceMatrix(classType, result)

    def displayFour(self):
        root = self.modelObj.btc.root
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
        print "\n\nTop 4 layers of the tree:"
        iteration = 1
        for entry in result:
            print "Layer ", iteration, ": ", entry    
            iteration += 1
    
    def display(self, node, depth = 0):
        if depth == 4:
            return
        print "Level: ", depth
        if node.attribute:
            print "word: ", node.attribute
        if node.decision:
            print "Decision node: ", "is spam" if node.decision is True else "is not spam"
        if node.left:
            if depth != 3:
                print "if '" + node.attribute + "' is not in document:"
            self.display(node.left, depth = depth + 1)
        if node.right:
            if depth != 3:
                print "if '" + node.attribute + "' is in document:"
            self.display(node.right, depth = depth + 1)
 
    def test(self):
        print "Testing On Tree (binary attributes)..."
        self.testDocuments('spam')
        self.testDocuments('notspam')
        self.displayAccuracy()
        self.displayFour()
        #root = self.modelObj.naryTree.root
        #self.display(root)
