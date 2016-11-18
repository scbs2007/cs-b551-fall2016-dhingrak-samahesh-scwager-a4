from training import TrainingBayesModel
from binaryTree import BinaryNode
 
bdt = BinaryNode()
#root
bdt.setAttribute("first")
bdt.insert("left", "second")
bdt.left.insert("left", decision = True)
bdt.insert("right", "third")
bdt.right.insert("left", "fourth")
bdt.display()
