from __future__ import division
import os, string, sys, math, pickle, re, heapq, random
from collections import Counter
from processCorpusUnknown import ProcessCorpusUnknown


class TrainingBayesModel:
    def __init__(self, directory, probKnowTopic = 1.):
        self.directory = directory
        self.probKnowTopic = probKnowTopic
        self.processCorpus = ProcessCorpusUnknown(directory, self.probKnowTopic)
        self.totTrainingDocs = 0
        self.docTopics = {} #probability of each of the 20 topics
        self.probWGivenTopic_Multinomial = Counter() #probability of each word given each topic
        self.probWGivenTopic_Bernoulli = Counter()
        self.probTopic = Counter()
        self.probWord = Counter() #probability of each word occurring in the corpus

    # Top 10 most associated with spam
    def mostAssociated(self, prob):
        return heapq.nlargest(10, prob, key=prob.get)

    def displayList(self, l):
        for entry in l:
            print entry + " ", 
        print "\n"
        
    def writeList(self, l):
        s = ""
        for entry in l:
            s += entry + " "
        return s

    def calculateProbWordsGivenTopic(self, probWGivenT, wordCount, pClass):
#         Takes into account the case where no words are in probWGivenT, i.e. probKnowTopic is zero or nearly zero
        w = 0 + sum([math.log(probWGivenT[entry]) for entry in wordCount if entry in probWGivenT])
        if w == 0: 
            return -1000000
        return w + math.log(pClass) + sum([math.log(1-probWGivenT[entry]) for entry in probWGivenT if entry not in wordCount])            

    def calculateProbTopicGivenWord(self, probWT, probT):
        probTW = Counter()
        for word, probW in self.probWord.items():
            probTW[word] = probWT[word] * probT / probW if word in probWT else 0
        return probTW
        
    def findTop10WordsGivenTopic(self):
        probTopicGivenWord = Counter()
        top10String = "Top 10 most associated words for each topic:\n"
        for topic, probT in self.probTopic.items():
            probWT = self.probWGivenTopic_Bernoulli[topic]
            probTopicGivenWord[topic] = self.calculateProbTopicGivenWord(probWT, probT)
            top10String += "\ntopic: " + topic + "\n" + self.writeList(self.mostAssociated(probTopicGivenWord[topic]))
#             print top10String
        return probTopicGivenWord, top10String

    def calculateProbWGivenTopic_Multinomial(self, wordCount, totWordsInClass):
        '''returns counter object reference for single topic'''
        prob = Counter()
        for entry in wordCount:
            prob[entry] = (wordCount[entry]+1)/(totWordsInClass+1)
        return prob
        
    def calculateProbWGivenTopics_Multinomial(self, wordCountInTopics, totDocWordCountInTopics):
        '''returns a counter with key: topic, value: counter object reference: probability of each word'''
        probWGivenTopic = Counter()
        for topic in wordCountInTopics:
            totWordsInTopic = totDocWordCountInTopics[topic][1] #total number of words in topic
            probWGivenTopic[topic] = self.calculateProbWGivenTopic_Multinomial(wordCountInTopics[topic], totWordsInTopic) #prob of each word occurring in topic
        return probWGivenTopic
        
    def calculateProbWGivenTopic_Bernoulli(self, wordCount, docCount):
        prob = Counter()
        for entry in wordCount:
            prob[entry] = (wordCount[entry]+1)/(docCount+2)
        return prob
        
    def calculateProbWGivenTopics_Bernoulli(self, wordCountInTopics, totDocWordCountInTopics):
        '''returns a counter with key: topic, value: counter object reference: probability of each word'''
        probWGivenTopic = Counter()
        for topic in wordCountInTopics:
            totDocsInTopic = totDocWordCountInTopics[topic][0] #total number of words in topic
            probWGivenTopic[topic] = self.calculateProbWGivenTopic_Bernoulli(wordCountInTopics[topic], totDocsInTopic) #prob of each word occurring in topic
        return probWGivenTopic
        
    def calculateProbTopic(self, totDocWordCountInTopics, totalDocs):
        '''probability of a given topic occurring, calculated based on number of examples for each topic'''
        prob = Counter()
        for entry in totDocWordCountInTopics:
            docCount = totDocWordCountInTopics[entry][0]
            prob[entry] = (docCount+1)/(totalDocs+2)
            #print docCount, totalDocs, prob[entry]
        return prob
        
    def calculateProbWord(self, wordFreqInCorpus, totalWords):
        prob = Counter()
        for entry, count in wordFreqInCorpus.items():
            prob[entry] = count/totalWords
        return prob
        
    def assignTopicsToUnknown(self, wordCountInEachDoc, topicIsFixed, probWGivenTopic, probTopic, changeThresh): 
        '''assign max prob topic to each doc whose topic is unknown'''
        change = 0 #true if a document changed topic assignment, i.e., convergence has not occurred
        for docID, (fixed, topicID) in topicIsFixed.items():
            if not fixed:
                oldtopicID = topicID
                wordCountInDoc = wordCountInEachDoc[docID]
                highestProbTopic, prob = "", -100000
                for topic, probT in probTopic.items():
                    probTopicGivenDoc = self.calculateProbWordsGivenTopic(probWGivenTopic[topic], wordCountInDoc, probT)
                    if probTopicGivenDoc > prob:
                        highestProbTopic, prob = topic, probTopicGivenDoc
#                         print "highestProbTopic", highestProbTopic, "prob", prob
                if not highestProbTopic: highestProbTopic = random.choice([topic for topic in probTopic]) #assign randomly
                topicIsFixed[docID] = (False, highestProbTopic)
                if highestProbTopic != topicID: change += 1 #an assignment was changed
        return True if change <= changeThresh else False
                
    def updateTotDocWordCountInTopics(self, totDocWordCountInTopics, totalWordsInEachDoc, topicIsFixed):
        '''updates the number of words and the number of documents for all topics as tuples'''
        updatedTotDocWordCountInTopics = Counter()
        for topic, (totDocs, totWords) in totDocWordCountInTopics.items(): #start with the known values
            for docID, (isFixed, docTopic) in topicIsFixed.items(): #add the count of the docs temporarily added to this topic
                if not isFixed and docTopic == topic:
                    totWords += totalWordsInEachDoc[docID]
                    totDocs += 1
            updatedTotDocWordCountInTopics[topic] = (totDocs, totWords)
        return updatedTotDocWordCountInTopics
                    
    def updateWordCountInTopicsBernoulli(self, wordCountInTopicsBernoulli, wordCountInEachDoc, topicIsFixed):
        updateWordCountInTopicsBernoulli = Counter()
        for topic, wordCount in wordCountInTopicsBernoulli.items(): #start with word count of fixed documents
            for docID, (isFixed, docTopic) in topicIsFixed.items(): #add the count of the docs temporarily assigned to this topic
                if not isFixed and docTopic == topic:
                    for entry in wordCountInEachDoc[docID]:
                        wordCount[entry] += 1
            updateWordCountInTopicsBernoulli[topic] = wordCount
        return updateWordCountInTopicsBernoulli

    def train(self):
        print "Training Bayes Net Model."
        print "Creating Vector."
        self.processCorpus.calculate()

        '''Initial values, probabilities'''
        '''These values will never change'''
        wordCountInEachDoc = self.processCorpus.wordCountInEachDoc # stores key: doc ID, value = counter object reference for the doc (counts only docs with *known* topic)
        wordFreqInCorpus = self.processCorpus.wordFreqInCorpus
        totalKnownDocs = self.processCorpus.totalDocs #total number of docs with *known* topic because used for the prob calculation
        totalWords = self.processCorpus.totalWords #total number of words in *all* docs, with known or unknown topic
        totalWordsInEachDoc = self.processCorpus.totalWordsInEachDoc #total number of words in *each* doc
        
        '''These values will be updated'''
        topicIsFixed = self.processCorpus.topicIsFixed #stores key = document ID, value = tuple: topic, whether topic was known in advance or only estimated
        totDocWordCountInTopics = self.processCorpus.docsAndWords # stores the number of words and the number of documents for all topics as tuples.
        totalDocs = totalKnownDocs 
        wordCountInTopicsMultinomial = self.processCorpus.wordCountMappingMultinomial # stores key = topic name, value = Counter object reference (count of each word's occurrence in all docs combined)
        wordCountInTopicsBernoulli = self.processCorpus.wordCountMappingBernoulli # stores key = topic name, value = Counter object reference (count of each word's occurrence in all docs combined)
        
        '''Initial probability calculations'''
        self.probTopic = self.calculateProbTopic(totDocWordCountInTopics, totalDocs)
        self.probWord = self.calculateProbWord(wordFreqInCorpus, totalWords)
        self.probWGivenTopic_Multinomial = self.calculateProbWGivenTopics_Multinomial(wordCountInTopicsMultinomial, totDocWordCountInTopics)
        self.probWGivenTopic_Bernoulli = self.calculateProbWGivenTopics_Bernoulli(wordCountInTopicsBernoulli, totDocWordCountInTopics)
        '''Iterations and updates'''
        '''assign topics to unassigned docs'''
        changeThresh = 100 #max number of docs that can change assignment in an iteration for the program to converge
        if probKnowTopic < 1: print "assigning topics to docs..."
        converged = self.assignTopicsToUnknown(wordCountInEachDoc, topicIsFixed, self.probWGivenTopic_Bernoulli, self.probTopic, changeThresh)
            
        while not converged:
            '''update counts'''
            print "new iteration: assigning topics to docs..."
            totalDocs = len(topicIsFixed) #now, all docs have been assigned
            updatedTotDocWordCountInTopics = self.updateTotDocWordCountInTopics(totDocWordCountInTopics, totalWordsInEachDoc, topicIsFixed) #update doc word count for each topic with newly assigned docs
    #         print "old", totDocWordCountInTopics, "updated", updatedTotDocWordCountInTopics
            updatedWordCountInTopicsBernoulli = self.updateWordCountInTopicsBernoulli(wordCountInTopicsBernoulli, wordCountInEachDoc, topicIsFixed) # stores key = topic name, value = Counter object reference (count of each word's occurrence in all docs combined)
            #not updating the multinomial for now'''
            '''update probabilities'''
            self.probTopic = self.calculateProbTopic(updatedTotDocWordCountInTopics, totalDocs)
            self.probWGivenTopic_Bernoulli = self.calculateProbWGivenTopics_Bernoulli(updatedWordCountInTopicsBernoulli, updatedTotDocWordCountInTopics)
            '''update document assignments once again'''
            converged = self.assignTopicsToUnknown(wordCountInEachDoc, topicIsFixed, self.probWGivenTopic_Bernoulli, self.probTopic, changeThresh)
        
        '''Processing the results'''
        probTopicGivenWord, s = self.findTop10WordsGivenTopic()
        with open("distinctive_words.txt", "w") as text_file:
            text_file.write(s)
      
