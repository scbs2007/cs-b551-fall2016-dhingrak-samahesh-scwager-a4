'''
#################################################################################################################
Formulation:
#################################################################################################################
Bayes Model:
We have used Counter objects to calculate almost everything in the assignment:
1. Raw count of the words in the corpus - for continuous naive bayes.
2. Number of documents in which the word appears - for binary naive bayes.
3. All the probabilities required in the P(S|Words) calculations.

For Tree model:
Each node of the tree for binary attribute stores:
1. attribute on which the split is taking place
2. decision -  decision for leaf node True (is spam), False - (not spam)
3. left, right - Store the left and right children of the node
4. indexSpamDocsWithWord - Contains the indexes of the docs in documentDictListSpam which are to be looked into for finding right successor
5. indexNotSpamDocsWithWord - Contains the indexes of the docs in documentDictListNotSpam which are to be looked into for finding right successor
6. indexSpamDocsWithoutWord - Contains the indexes of the docs in documentDictListSpam which are to be looked into for finding left successor
7. indexNotSpamDocsWithoutWord - Contains the indexes of the docs in documentDictListNotSpam which are to be looked into for finding left successor
8. ignoreWords - Set containing words out of consideration for entropy calculation for the next iteration

Each node of the tree for raw count attribute stores:
1. attribute - Attribute is the chosen word on which to split
2. decision - decision for leaf node True (is spam), False - (not spam)
3. threshold - Value of best word at which to split
3. left, right - Store the left and right children of the node
4. leftDataAndClass - List of tuples (Counter - containing word:freq, class of document). Documents which are to be looked into for finding the left successor
5. rightDataAndClass - List of tuples (Counter - containing word:freq, class of document). Documents which are to be looked into for finding the right successor
6. ignoreWords - Set containing words out of consideration for entropy calculation for the next iteration

Tree Model:
We have implemented the ID3 algorithm for the binary attribute and the C4.5 Algorithm for the continuous attributes.
1. For ID3 the best splits are decided based on the entropy of each word which takes into account only the counts of the presence and absence of words in docs.
2. For C4.5 the best splits are decided taking into consideration the lowest entropy of each word for each unique frequency of the word.
   5 fold cross validations have been done to find the optimal height of the tree.

#################################################################################################################
Description of how the program works:
#################################################################################################################
The program has been modularised in many files:
1. spam.py contains the part where the program will start execution
2. processCorpus.py deals with all the file reads for both the bayes and the tree models; and the calculation of raw word counts in the corpus.
3. treeTraining.py deals with the training of the dt. It splits execution for binary and continuous attribute trees to:
    1. binaryTree.py - The ID3 algorithm has been implemented in here. It takes the help of:
       binaryNode.py which deals with each node for binary attribute nodes.
    2. binaryTreeContinuous.py - The C4.5 algorithm has been implemented here. It takes the help of:
       binaryNodeContinuous.py which deals with each node for continuous attribute nodes.
4. bayesTraining.py deals with the calculation of the probabilities of the words required for the bayes model.
5. treeTesting.py deals with the testing of the tree models. It splits execution to:
    1. btContinuousTesting.py which deals with testing the continuous tree.
    2. btTesting.py which deals with the testing of the binary attribute tree.
6. bayesTesting.py deals with the testing of the bayes model.

#################################################################################################################
Difficulty faced:
#################################################################################################################
1. We found after a lot of experimenting that the bayes model is highly dependent on the words that are taken into consideration.
At the beginning when we started on the assignment we were getting around 90% accuracy for binary attribute values.
But at present after we have filtered out a lot of words (stop words and unnecessary html tags, email headers) the accuracy percentage has reduced drastically.
So determining which words to filter out was a huge problem. We had to stick with the present result.

Moreover if we do not add all the present filters, the top 10 words least and most associated with spam all turn out to be junk words/ words specific to email/ html tags.

2. Choosing the odds ratio via experimenting was also difficult. This took a great amount of time.
3. 5 fold cross validation has been done to find the optimal heiht of the tree. This also took a lot of time.

#################################################################################################################
Result:
#################################################################################################################
For Bayes Model:

Testing with binary vector...

Accuracy Percentage:  62.02
Confidence Matrix:
True Positive:  1023
False Negative:  808
False Positive:  162
True Negative:  561


Testing with raw count vector...

Accuracy Percentage:  90.45
Confidence Matrix:
True Positive:  1074
False Negative:  133
False Positive:  111
True Negative:  1236


Top 10 words most associated with spam:
email  free  new  money  business  list  microsoft  information  receive  internet

Top 10 words least associated with spam:
geneva  chris  cnet  weblog  blog  matthias  habeas  folder  unseen  bug


For Tree Model:

Testing On Tree (binary attributes)...

Accuracy Percentage:  94.4
Confidence Matrix:
True Positive:  1126
False Negative:  84
False Positive:  59
True Negative:  1285


Top 4 layers of the tree: (Left branch - Word was absent. Right branch - Word was present.)
Layer  1 :  ['jalapeno']
Layer  2 :  ['reported', 'receive']
Layer  3 :  ['wrote', 'aging', 'click', 'form']
Layer  4 :  ['reserved', 'customer', 'rating', None, 'reply', 'discussion', 'offer', None]
Testing On Tree (binary attributes)...


Accuracy Percentage:  94.17
Confidence Matrix:
True Positive:  1122
False Negative:  86
False Positive:  63
True Negative:  1283


Top 4 layers of the tree:
Layer  1 :  ['jalapeno']
Layer  2 :  ['reported', 'receive']
Layer  3 :  ['footer', 'aging', 'click', 'form']
Layer  4 :  ['group', None, 'rating', None, 'reply', 'discussion', 'offer', None]



Which Technique works best?
This is debatable. As pointed out earlier the filtering of the words plays a huge role in the accuracy of the models.
For us the bayes model was giving much better results when we had not added a lot of word filters.
Did not get time to experiment further. Lost track of the initial word filters which gave great results. :(
#################################################################################################################
Other Comments:
#################################################################################################################
- The bayes binary model is found to be always less accurate than the continuous model. This can be because the binary bayes ignores the raw counts of the words in 
the corpus.
- The dt with binary attribute values is found to always be more accurate than the continuous dt. This can be because the continuous attribute tree is prone
to quickly overfit.
- The binary bayes model testing takes a lot of time because for each test document all words' (in the training corpus) P(S|Wi) are taken into 
calculation for P(S|Words).
- The training of the binary tree which considers continuous attribute values takes a lot of time because for each word each of its' unique frequency values
in the corpus are taken into consideration for finding the min entropy.

'''
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
    decisionTree = TrainingTreeModel(directory)
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
        print "Training Done. Storing Model..."
        pickle.dump(decisionTree, open(modelFile, "wb"))
        print "Tree Model stored in ", modelFile
    elif mode == "test":
        testingTree(directory)
    else:
        print "Incorrect Mode entered: ", mode
else:
    print "Incorrect Technique entered: ", technique
