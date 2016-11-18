from binaryNode import BinaryNode

class BinaryTree:
    def __init__(self, probabilities):
        self.prob = probabilities

    def train(self):
        probWGivenNotSpam = self.prob.probWGivenSpam_Bernoulli
        probWGivenSpam = self.prob.probWGivenSpam_Bernoulli
        wordCountNotSpam = self.prob.wordCountInNotSpam_Bernoulli 
        wordCountSpam = self.prob.wordCountInSpam_Bernoulli
        pass


    def decisionTreeLearning_Bernoulli(self):
        '''uses self.probWGivenNotSpam_Bernoulli and self.probWGivenSpam_Bernoulli
        when only creatingVector has been run on them.
        need to decide whether to keep the recursive helper function
        p. 702 - 704 of textbook '''
        probWGivenNotSpam_Bernoulli = self.prob.probWGivenSpam_Bernoulli
        probWGivenSpam_Bernoulli = self.prob.probWGivenSpam_Bernoulli
        return
    
    def decisionTreeLearningRecursive_Bernoulli(self):
        
        return
        
    def importance(self):
        #calculate information gain
        return
 
