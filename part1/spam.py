import sys, os, pickle
from training import TrainModel
from testing import TestModel

mode, technique, directory, modelFile = sys.argv[1:5]
if technique == "bayes":
    if mode == "train":
        trainingObj = TrainModel(directory)
        trainingObj.train()
        pickle.dump(trainingObj, open(modelFile, "wb"))
        print "Training Done. Model stored in ", modelFile
 
    elif mode == "test":
        trainedObj = pickle.load(open(modelFile, "rb"))
        print "Found Trained Model."  
        testingObj = TestModel(directory)
        testingObj.testDocuments(trainedObj)
    else:
        print "Mode Entered is incorrect!"
 
elif technique == "dt":
    if mode == "train":
        pass
    elif mode == "test":
        pass
    else:
        print "Mode Entered is incorrect!"

