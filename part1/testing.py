import os, string, math

class TestModel:
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
        #return sum([math.log(probWGivenS[entry]) for entry in probWGivenS if entry in wordCount]) + math.log(pClass)
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

    def testModel(self, classType, pSpam, pNotSpam, probWGivenNotSpam, probWGivenSpam, confidenceMatrix, threshold, fetchTokens):
        directoryPath = self.directory + '/test/' + classType
        
        for fileName in os.listdir(directoryPath):
            with open(directoryPath + '/' + fileName) as document:
                wordCount = fetchTokens(document)

                probIsSpam = self.calculateProbWordsGivenS(probWGivenNotSpam, wordCount, pNotSpam)
                probIsNotSpam = self.calculateProbWordsGivenS(probWGivenSpam, wordCount, pSpam)
                
                #print "\nFile Name: ", fileName, "Type: ", classType
                oddsRatio = probIsSpam/probIsNotSpam
                #print "Odds Ratio: ", oddsRatio
                
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

    def testDocuments(self, modelObj):
        pSpam = modelObj.pSpam
        pNotSpam = modelObj.pNotSpam
        probWGivenNotSpam_Bernoulli = modelObj.probWGivenNotSpam_Bernoulli
        probWGivenSpam_Bernoulli = modelObj.probWGivenSpam_Bernoulli
        probWGivenNotSpam_Multinomial = modelObj.probWGivenNotSpam_Multinomial
        probWGivenSpam_Multinomial = modelObj.probWGivenSpam_Multinomial
        confidenceMatrix_Bernoulli = [0, 0, 0, 0]
        confidenceMatrix_Multinomial = [0, 0, 0, 0]      

        # Testing Bernoulli Model
        threshold = 1.00009 
        # Testing spam Folder
        print "Testing with binary vector..."
        self.testModel('spam', pSpam, pNotSpam, probWGivenNotSpam_Bernoulli, probWGivenSpam_Bernoulli, confidenceMatrix_Bernoulli, threshold, modelObj.fetchTokens) 
        # Testing notspam Folder
        self.testModel('notspam', pSpam, pNotSpam, probWGivenNotSpam_Bernoulli, probWGivenSpam_Bernoulli, confidenceMatrix_Bernoulli, threshold, modelObj.fetchTokens)
        self.displayAccuracy(confidenceMatrix_Bernoulli)
     
        # Testing Multinomial Model
        threshold = 1.00009 
        print "Testing with raw count vector..."
        self.testModel('spam', pSpam, pNotSpam, probWGivenNotSpam_Multinomial, probWGivenSpam_Multinomial, confidenceMatrix_Multinomial, threshold, modelObj.fetchTokens)
        self.testModel('notspam', pSpam, pNotSpam, probWGivenNotSpam_Multinomial, probWGivenSpam_Multinomial, confidenceMatrix_Multinomial, threshold, modelObj.fetchTokens)
        self.displayAccuracy(confidenceMatrix_Multinomial)


