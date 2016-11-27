from bayesTraining import TrainingBayesModel

def main():
    tb = TrainingBayesModel("./", probKnowTopic = 0.7)
    tb.train()
    
main()