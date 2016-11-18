from naryNode import NaryNode

class NaryTree:
    def __init__(self, probabilities):
        self.prob = probabilities
    
    def train(self):
        probWGivenNotSpam = self.prob.probWGivenSpam_Multinomial
        probWGivenSpam = self.prob.probWGivenSpam_Multinomial
        wordCountNotSpam = self.prob.wordCountInNotSpam_Multinomial
        wordCountSpam = self.prob.wordCountInSpam_Multinomial
        pass

