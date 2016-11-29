from bayesTraining import TrainingBayesModel

'''note: when probKnowTopic is 0 or very small, the topic names may not match the topic of the documents assigned
to this topic indes, i.e. all topics related to "forsale" might be grouped in the topic category named "windows".'''

def main():
    tb = TrainingBayesModel("./", probKnowTopic = 1)
    tb.train()
    
main()