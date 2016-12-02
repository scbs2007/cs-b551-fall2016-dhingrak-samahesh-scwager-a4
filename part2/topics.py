import sys, os, pickle
from bayesTraining import TrainingBayesModel
from bayesTesting import TestingBayesModel

'''

For each programming problem, please include a detailed comments section at the top of your code that describes:
 
(1) a description of how you formulated the problem, including precisely defining the abstractions; 
The probabilities are computed as for part 1, using the bernoulli version of naive bayes, except that the class count
is 20 instead of 2. The only difference is that when the probability of knowing a topic is less than 1, the model needs
to be trained iteratively. To do this, we:
    a. compute P(T), P(W|T), P(W) using available training data
    while the document assignments have not converged:
        b. assign documents to the most likely topic as follows: 
            t = argmax_T( prod( P(w|T) for w in doc) * prod( 1-P(w|T) for w not in doc) * P(T)
        c. update P(T), P(W|T), P(W)
        
(2) a brief description of how your program works; 
To decide when the document assignments have converged, we set changeThresh in bayesTraining.train as the max number 
of docs that can change assignment in an iteration. Ideally, changeThresh would be zero, but could this take too long.

note: when probKnowTopic is 0 or very small, the topic names may not match the topic of the documents assigned
to this topic indes, i.e. all topics related to "forsale" might be grouped in the topic category named "windows".

(3) a discussion of any problems, assumptions, simplifications, and/or design decisions you made; and 
We decided to store every document as a word dictionary, despite the memory cost, instead of reading every document from
a file every time the probability of a topic given the document was computed. Still, the program takes a long time to 
compute the Bernoulli distribution.

While the top 10 word lists are convincing, the accuracy is low. Documents get more likely assigned to certain topics than
others, no matter what the true topic is. The bug remains to be discovered.

(4) answers to any questions asked below in the assignment. '''


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