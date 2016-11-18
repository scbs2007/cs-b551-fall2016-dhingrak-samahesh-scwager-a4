from binaryNode import BinaryNode

class BinaryTree:
    def __init__(self, probabilities):
        self.prob = probabilities
        self.root = None

    def train(self):
        probWGivenNotSpam = self.prob.probWGivenSpam_Bernoulli
        probWGivenSpam = self.prob.probWGivenSpam_Bernoulli
        wordCountNotSpam = self.prob.wordCountInNotSpam_Bernoulli 
        wordCountSpam = self.prob.wordCountInSpam_Bernoulli
        self.decisionTreeLearning_Bernoulli(wordCountNotSpam, wordCountSpam)

    def decisionTreeLearning_Bernoulli(self, wordCountNotSpam, wordCountSpam, maxHeight = 1):
        return
#         probWGivenNotSpam_Bernoulli = self.prob.probWGivenSpam_Bernoulli
#         probWGivenSpam_Bernoulli = self.prob.probWGivenSpam_Bernoulli
        rootWord = self.mostImportantWord(wordCountNotSpam, wordCountSpam)
        self.root = BinaryNode(attribute = rootWord)
#         leftWordCountNotSpam = [wc for wordCountNotSpam if ]
#         leftWordCountSpam = []
#         rightWordCountNotSpam = []
#         rightWordCountSpam = []
        leftCondition = {rootWord: 0}
        rightCondition = {rootWord: 1}
        self.root.left.decisionTreeLearningHelp_Bernoulli(self, wordCountNotSpam, wordCountSpam, leftCondition, maxHeight-1)
        self.root.right.decisionTreeLearningHelp_Bernoulli(self, wordCountNotSpam, wordCountSpam, rightCondition, maxHeight-1)
        return self.root
        
    def decisionTreeLearningHelp_Bernoulli(self, wordCountNotSpam, wordCountSpam, condition, remainingHeight):
        return
        
    def mostImportantWord(self, localWordCountNotSpam, localWordCountSpam):
        return localWordCountSpam[0]
 
