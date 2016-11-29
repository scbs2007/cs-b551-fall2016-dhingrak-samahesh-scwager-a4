import sys, os, pickle
from bayesTraining import TrainingBayesModel
from bayesTesting import TestingBayesModel

'''note: when probKnowTopic is 0 or very small, the topic names may not match the topic of the documents assigned
to this topic indes, i.e. all topics related to "forsale" might be grouped in the topic category named "windows".'''

def trainingBayes(modelFile, directory, fraction):
    trainingObj = TrainingBayesModel(directory, fraction)
    trainingObj.train()
    return trainingObj

def testingBayes(directory):
    trainedObj = pickle.load(open(modelFile, "rb"))
    print "Found Trained Bayes Model."
    testingObj = TestingBayesModel(directory)
    testingObj.testDocuments(trainedObj)

mode, directory, modelFile = sys.argv[1:4]
if mode == "train":
    fraction = float(sys.argv[4])
    trainingObj = trainingBayes(modelFile, directory, fraction)
    pickle.dump(trainingObj, open(modelFile, "wb"))
    print "Training Done. Bayes Model stored in ", modelFile
elif mode == "test":
    testingBayes(directory)
else:
    print "Incorrect Mode entered: ", mode