from __future__ import division
import os, string, math, heapq
from collections import Counter

#ob = []
#om = []

class TestingBayesModel:
    def __init__(self, directory):
        self.directory = directory

    def displayAccuracy(self, confidenceMatrix):
        print "\n\nAccuracy Percentage: ", round((confidenceMatrix[0] + confidenceMatrix[3]) * 100.0 / sum(confidenceMatrix), 2)
        print "Confidence Matrix: "
        print "True Positive: ", confidenceMatrix[0]
        print "False Negative: ", confidenceMatrix[1] 
        print "False Positive: ", confidenceMatrix[2] 
        print "True Negative: ", confidenceMatrix[3] 

    def calculateProbWordsGivenS(self, probWGivenS, wordCount, pClass):
        # For now considering only words present in the training data.
        # Also for a particular test document's words - taking into consideration only P(W|S) and not 1 - P(W|S)
        return sum([math.log(probWGivenS[entry]) for entry in wordCount if entry in probWGivenS]) + math.log(pClass)


        result = 0
        for entry in probWGivenS:
            if entry in wordCount:
                result += math.log(probWGivenS[entry])
                #print entry, probWGivenS[entry]
            else:
                if probWGivenS[entry] > 0:
                    #print entry, probWGivenS[entry]
                    result += math.log(1 - probWGivenS[entry])
                else:
                    # Word wasn't there in training data. Ignoring. TODO: Do not ignore?
                    pass
                #print entry, 1 - probWGivenS[entry]
        #print min(probWordsGivenS)
        return result + math.log(pClass)

    def bernoulliThresh(self, oddsRatio, confidenceMatrix, threshold, classType):
        if oddsRatio > threshold:
            #print "Predicted - Spam"
            if classType == 'spam':
                confidenceMatrix[0] += 1
            if classType == 'notspam':
                confidenceMatrix[1] += 1
        else:
            #print "Predicted - Not Spam"
            if classType == 'spam':
                confidenceMatrix[2] += 1
            if classType == 'notspam':
                confidenceMatrix[3] += 1
        
    def multinomialThresh(self, oddsRatio, confidenceMatrix, threshold, classType):
        if oddsRatio > threshold:
            #print "Predicted - Spam"
            if classType == 'spam':
                confidenceMatrix[0] += 1
            if classType == 'notspam':
                confidenceMatrix[1] += 1
        else:
            #print "Predicted - Not Spam"
            if classType == 'spam':
                confidenceMatrix[2] += 1
            if classType == 'notspam':
                confidenceMatrix[3] += 1

    def testModel(self, classType, pSpam, pNotSpam, probWGivenNotSpam, probWGivenSpam, confidenceMatrix, threshold, fetchTokens, modelName):
        directoryPath = self.directory + '/test/' + classType
        
        for fileName in os.listdir(directoryPath):
            with open(directoryPath + '/' + fileName) as document:
                wordCount = fetchTokens(document)

                probIsSpam = self.calculateProbWordsGivenS(probWGivenNotSpam, wordCount, pNotSpam)
                probIsNotSpam = self.calculateProbWordsGivenS(probWGivenSpam, wordCount, pSpam)
                
                #print "\nFile Name: ", fileName, "Type: ", classType
                oddsRatio = probIsSpam/probIsNotSpam
                #print "Odds Ratio: ", oddsRatio
               
                if modelName == 'bernoulli':
                    #ob.append(oddsRatio)
                    self.bernoulliThresh(oddsRatio, confidenceMatrix, threshold, classType)
                elif modelName == 'multinomial':
                    #om.append(oddsRatio)
                    self.multinomialThresh(oddsRatio, confidenceMatrix, threshold, classType)
                    
    # Top 10 least associated with spam
    def leastAssociated(self, prob):
        return heapq.nsmallest(10, prob, key=prob.get)

    # Top 10 most associated with spam
    def mostAssociated(self, prob):
        return heapq.nlargest(10, prob, key=prob.get)

    def displayList(self, l):
        for entry in l:
            print entry + " ", 
        print "\n"

    def findTop10(self, model):
        probWS = model.probWGivenSpam_Multinomial
        probS = model.pSpam
        probSW = Counter()

        for word in model.processCorpus.allWordsInCorpus:
            probW = (model.processCorpus.wordCountInSpam_Multinomial[word] + model.processCorpus.wordCountInNotSpam_Multinomial[word])/ \
                (model.processCorpus.totWordsInNotSpam + model.processCorpus.totWordsInSpam)
            probSW[word] = probWS[word] * probS / probW

        print "Top 10 words most associated with spam: "
        self.displayList(self.mostAssociated(probSW))

        print "Top 10 words least associated with spam: "
        self.displayList(self.leastAssociated(probSW))
        '''
        prob1 = model.probWGivenSpam_Multinomial
        prob2 = model.probWGivenSpam_Bernoulli
        
        prob3 = model.probWGivenNotSpam_Multinomial
        prob4 = model.probWGivenNotSpam_Bernoulli

        probSpam = model.pSpam
        pNotSpam = model.pNotSpam
        
        set1 = self.mostAssociated(prob1)
        set2 = self.mostAssociated(prob2)
        print "Top 10 words most associated with spam: " 
        print "Multinomial: "
        self.displayList(set1)
        print "Bernoulli: "
        self.displayList(set2)

        set3 = self.leastAssociated(prob3)
        set4 = self.leastAssociated(prob4)
        print "\n\nTop 10 words least associated with spam: "
        print "Multinomial: "
        self.displayList(set3)
        print "Bernoulli: "
        self.displayList(set4)
        '''
             
    def testDocuments(self, modelObj):
        pSpam = modelObj.pSpam
        pNotSpam = modelObj.pNotSpam
        probWGivenNotSpam_Bernoulli = modelObj.probWGivenNotSpam_Bernoulli
        probWGivenSpam_Bernoulli = modelObj.probWGivenSpam_Bernoulli
        probWGivenNotSpam_Multinomial = modelObj.probWGivenNotSpam_Multinomial
        probWGivenSpam_Multinomial = modelObj.probWGivenSpam_Multinomial

        # 0 - true positive, 1 - false negative, 2 - false positive, 3 - true negative
        confidenceMatrix_Bernoulli = [0, 0, 0, 0]
        confidenceMatrix_Multinomial = [0, 0, 0, 0]      

        # Testing Bernoulli Model
        threshold = 0.4509 

        # Testing spam Folder
        print "Testing with binary vector..."
        self.testModel('spam', pSpam, pNotSpam, probWGivenNotSpam_Bernoulli, probWGivenSpam_Bernoulli, confidenceMatrix_Bernoulli, threshold, modelObj.processCorpus.fetchTokens, 'bernoulli') 

        # Testing notspam Folder
        self.testModel('notspam', pSpam, pNotSpam, probWGivenNotSpam_Bernoulli, probWGivenSpam_Bernoulli, confidenceMatrix_Bernoulli, threshold, modelObj.processCorpus.fetchTokens, 'bernoulli')
        self.displayAccuracy(confidenceMatrix_Bernoulli)
        
        # Testing Multinomial Model
        threshold = 1.5808 #0.595271488128
        print "Testing with raw count vector..."
        self.testModel('spam', pSpam, pNotSpam, probWGivenNotSpam_Multinomial, probWGivenSpam_Multinomial, confidenceMatrix_Multinomial, \
                        threshold, modelObj.processCorpus.fetchTokens, 'multinomial')

        self.testModel('notspam', pSpam, pNotSpam, probWGivenNotSpam_Multinomial, probWGivenSpam_Multinomial, confidenceMatrix_Multinomial, \
                        threshold, modelObj.processCorpus.fetchTokens, 'multinomial')
        self.displayAccuracy(confidenceMatrix_Multinomial)
        self.findTop10(modelObj)
        #print "OB: ", min(ob)
        #print "OB: max", max(ob)
        #print "OM: ", min(om)
        #print "OM: max ", max(om)


