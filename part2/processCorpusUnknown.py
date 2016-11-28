import re, os, string
from collections import Counter
import numpy as np

'''
All file reading in this class
'''

class ProcessCorpusUnknown:
    def __init__(self, directory, probKnowTopic = 1.):
        self.directory = directory
        self.docsAndWords = Counter() # stores the number of words and the number of documents for all topics as tuples.
        self.wordCountMapping = Counter() # stores key = topic name, value = Counter object reference (count of each word's occurrence in all docs combined)
        self.totalDocs = 0
        self.probKnowTopic = probKnowTopic #probability that we know the topic of a given document
        self.wordCountInEachDoc = Counter() #stores key = document ID, value = Counter object reference (count of each word's occurrence in the given doc) 
        self.topicIsFixed = {} #stores key = document ID, value = tuple: topic, whether topic was known in advance or only estimated
        self.unknownWordCount = 0
        self.unknownDocCount = 0
  
        # http://xpo6.com/list-of-english-stop-words/
        self.stopWords = set(["a", "about", "above", "across", "after", "afterwards", "again", "against", "all", "almost", "alone", "along", "already", "also", \
                        "although", "always", "am", "among", "amongst", "amoungst", "amount", "an", "and", "another", "any", "anyhow", "anyone", "anything",\
                        "anyway", "anywhere", "are", "around", "as", "at", "back", "be", "became", "because", "become", "becomes", "becoming", "been", "before", \
                        "beforehand", "behind", "being", "below", "beside", "besides", "between", "beyond", "bill", "both", "bottom", "but", "by", "call", "can", \
                        "cannot", "cant", "co", "con", "could", "couldnt", "cry", "de", "describe", "detail", "do", "done", "down", "due", "during", "each", "eg", \
                        "eight", "either", "eleven", "else", "elsewhere", "empty", "enough", "etc", "even", "ever", "every", "everyone", "everything", \
                        "everywhere", "except", "few", "fifteen", "fify", "fill", "find", "fire", "first", "five", "for", "former", "formerly", "forty", "found", \
                        "four", "from", "front", "full", "further", "get", "give", "go", "had", "has", "hasnt", "have", "he", "hence", "her", "here", "hereafter",\
                        "hereby", "herein", "hereupon", "hers", "herself", "him", "himself", "his", "how", "however", "hundred", "ie", "if", "in", "inc", \
                        "indeed", "interest", "into", "is", "it", "its", "itself", "keep", "last", "latter", "latterly", "least", "less", "ltd", "made", "many", \
                        "may", "me", "meanwhile", "might", "mill", "mine", "more", "moreover", "most", "mostly", "move", "much", "must", "my", "myself", "name", \
                        "namely", "neither", "never", "nevertheless", "next", "nine", "no", "nobody", "none", "noone", "nor", "not", "nothing", "now", "nowhere", \
                        "of", "off", "often", "on", "once", "one", "only", "onto", "or", "other", "others", "otherwise", "our", "ours", "ourselves", "out", "over",\
                        "own","part", "per", "perhaps", "please", "put", "rather", "re", "same", "see", "seem", "seemed", "seeming", "seems", "serious", "several",\
                        "she", "should", "show", "side", "since", "sincere", "six", "sixty", "so", "some", "somehow", "someone", "something", "sometime", \
                        "sometimes", "somewhere", "still", "such", "system", "take", "ten", "than", "that", "the", "their", "them", "themselves", "then", \
                        "thence", "there", "thereafter", "thereby", "therefore", "therein", "thereupon", "these", "they", "thick", "thin", "third", "this", \
                        "those", "though", "three", "through", "throughout", "thru", "thus", "to", "together", "too", "top", "toward", "towards", "twelve", \
                        "twenty", "two", "un", "under", "until", "up", "upon", "us", "very", "via", "was", "we", "well", "were", "what", "whatever", "when", \
                        "whence", "whenever", "where", "whereafter", "whereas", "whereby", "wherein", "whereupon", "wherever", "whether", "which", "while", \
                        "whither", "who", "whoever", "whole", "whom", "whose", "why", "will", "with", "within", "without", "would", "yet", "you", "your", \
                        "yours", "yourself", "yourselves", "the", \
                        ])
 
        # Words related to email
        self.unwanted = set(['From:', 'Subject:', 'Summary:', 'Keywords:', 'Expires:', 'Distribution:', 'Organization:', 'Supersedes:', 'Lines:', 'Archive-name:', \
                        'Alt-atheism-archive-name:', 'Last-modified:', 'Version:', 'NNTP-Posting-Host:', 'Re:', 'Nntp-Posting-Host:', 'X-Mailer:', 'Reply-To:', \
                        'Article-I.D.:', 'X-Newsreader:', 'In-Reply-To:', 'Distribution:', \
                        'Originator:', 'Organization:',  'Keywords:', 'News-Software:', 'VNEWS', 'VAX/VMS', 'rusnews', 'newtout', \
                        'sun', 'mon', 'tue', 'wed', 'thu', 'fri', 'sat',\
                        'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec' \
                        ])

        # If token contains any of these - ignore it.
        self.remove = set(['!', '\\', '/', ',', '.', '@', '=', '[', ']', '(', ')', ':', ';', '?', '^', '{', '}', '|', '<', '>', '"', '#', '%', '&', '+', '`', '~',\
                             '0', '1', '2', '3', '4', '5', '6', '7', '8', '9'])



    def splitOnPunctuations(self, token, regex):
        return regex.sub('#', token).split('#')
    
    def checkUnwanted(self, token):
        if token in self.unwanted:
            return False 
        return True
        
    def toConsiderOrNotToConsider(self, word):

        if word in self.unwanted:
            return False 

        if word in self.stopWords:
            return False
        
        if word == '':
            return False
       
        if any(ch in self.remove for ch in word):
            return False 

        if str.isdigit(word):
            return False
         
        if len(word) > 15 or len(word) < 3:
            return False

        return True

    # This function is used in bayesTesting.py too
    def fetchTokens(self, document):
        # TODO 
        tokens = []
        #regex = re.compile('[%s]' % re.escape(string.punctuation))
        flag = True
        for token in document.read().split():
            # Remove HTML tags and URLs
            if self.checkUnwanted(token) == False or ('<' in token or '>' in token) or token.startswith('http://'):
                #print token
                continue

            #    for entry in self.splitOnPunctuations(token, regex):
            token = str.lower(str.lstrip(str.rstrip(token, string.punctuation), string.punctuation))
            if self.toConsiderOrNotToConsider(token):
                    tokens.append(token)
        return tokens

    # Counts w|c; total number of words in a document
    def countWordsInDocument(self, wordFreq, document):
        count = 0 # Counts total number of words in document
        docWordFreq = Counter()
        for entry in self.fetchTokens(document):
            count += 1
            wordFreq[entry] += 1
            docWordFreq[entry] += 1
        return count, docWordFreq
        
    def creatingVector(self, wordFreq, directoryPath):
        ''' read in words from file and store information about each individual doc. 
        choose randomly with given probability whether topic is known or unknown.
        if known, update topic information. if not, update count of unknown documents.'''
        
        docCount = 0 # Total documents for this topic in training data
        wordCount = 0 # Count of words in this topic
        # Reading all files in topic subdirectory
        for fileName in os.listdir(directoryPath):
            with open(directoryPath + '/' + fileName) as document:
                docID = directoryPath + '/' + fileName
                knowTopic = True if np.random.binomial(1, self.probKnowTopic) == 1 else False #determine whether topic is known
                docWordCount, docWordFreq = self.countWordsInDocument(wordFreq, document) #total number of words in doc, word frequency counter
                if knowTopic:
                    wordCount += docWordCount
                    docCount += 1
                else:
                    self.unknownWordCount += docWordCount
                    self.unknownDocCount += 1
                self.wordCountInEachDoc[docID] = docWordFreq #store word count data for this individual document
                '''print "file: ", fileName, "wordCountInDoc", self.wordCountInEachDoc[fileName]
                quit() '''
                self.topicIsFixed[docID] = (True, docID) if knowTopic else (False, "")
        return (docCount, wordCount)

    def calculate(self):
        topics = [os.path.join(self.directory, topicName) for topicName in os.listdir(self.directory) if os.path.isdir(os.path.join(self.directory, topicName))]
        self.unknownWordCount = 0
        self.unknownDocCount = 0
                        
        for topic in topics:
            print "Counting words in topic: ", topic
            wordFreq = Counter()
            self.docsAndWords[topic] = self.creatingVector(wordFreq, topic)
            self.wordCountMapping[topic] = wordFreq
        self.totalDocs = len(self.topicIsFixed)
        '''print "topicIsFixed", self.topicIsFixed
        print "unknownWordCount, unknownDocCount", self.unknownWordCount, self.unknownDocCount'''
        print "Words counted in all documents in all topics!"
