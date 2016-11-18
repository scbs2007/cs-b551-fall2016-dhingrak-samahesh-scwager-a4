import sys, os, pickle
from bayesTraining import TrainingBayesModel
from bayesTesting import TestingBayesModel
from treeTraining import TrainingTreeModel
from treeTesting import TestingTreeModel

def trainingBayes(modelFile, directory):
    trainingObj = TrainingBayesModel(directory)
    trainingObj.train()
    return trainingObj

def testingBayes(directory):
    trainedObj = pickle.load(open(modelFile, "rb"))
    print "Found Trained Bayes Model."
    testingObj = TestingBayesModel(directory)
    testingObj.testDocuments(trainedObj)

def trainingTree(modelFile, directory):
    bayesObj = trainingBayes(modelFile, directory)
    decisionTree = TrainingTreeModel(bayesObj)
    decisionTree.train()
    return decisionTree

def testingTree(directory):
    trainedTree = pickle.load(open(modelFile, "rb"))
    print "Found Trained Tree Model."
    testingObj = TestingTreeModel(directory)
    testingObj.testDocuments(trainedTree)

mode, technique, directory, modelFile = sys.argv[1:5]
if technique == "bayes":
    if mode == "train":
        trainingObj = trainingBayes(modelFile, directory)
        pickle.dump(trainingObj, open(modelFile, "wb"))
        print "Training Done. Bayes Model stored in ", modelFile
    elif mode == "test":
        testingBayes(directory)
    else:
        print "Incorrect Mode entered: ", mode
elif technique == "dt":
    if mode == "train":
        decisionTree = trainingTree(modelFile, directory)
        pickle.dump(decisionTree, open(modelFile, "wb"))
        print "Training Done. Tree Model stored in ", modelFile
    elif mode == "test":
        testingTree(directory)
    else:
        print "Incorrect Mode entered: ", mode
else:
    print "Incorrect Technique entered: ", technique
