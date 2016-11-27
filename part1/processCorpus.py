import re, os, string
from collections import Counter

'''
All file reading in this class
'''

class ProcessCorpus:
    def __init__(self, directory):
        self.directory = directory

        # Key = Word, Value = Count of the documents which contain the word
        self.wordCountInNotSpam_Bernoulli = Counter()
        self.wordCountInSpam_Bernoulli = Counter() 
        
        # Key = Word, Value = Number of occurences in training data 
        self.wordCountInNotSpam_Multinomial = Counter()
        self.wordCountInSpam_Multinomial = Counter() 

        self.allWordsInCorpus = set() 
        self.totNotSpamDocs = 0
        self.totWordsInNotSpam = 0
        self.totSpamDocs = 0
        self.totWordsInSpam = 0
        self.totTrainingDocs = 0
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
                        "yours", "yourself", "yourselves", "the" \
                        ])
        # Words related to email
        self.unwanted = set(['(Postfix)', 'Apr', 'Aug', 'Content-Transfer-Encoding:', 'Content-Type:', 'Date:', 'Dec', 'Delivered-To:', 'ESMTP', 'Errors-To:', \
                     'Feb', 'Forwarded-by:', 'From:', 'IMAP', 'In-Reply-To:', 'Jan', 'Jul', 'Jun', 'List-Archive:', 'List-Help:', 'List-Id:', 'List-Post:', \
                     'List-Subscribe:', 'List-Unsubscribe:', 'MIME-Version:', 'Mailing-List:', 'Mar', 'May', 'Message-Id:', 'Nov', 'Oct', 'Old-Return-Path:',\
                     'Organization:', 'Precedence:', 'RPM-List', 'Received:', 'References:', 'Reply-To:', 'Resent-Date:', 'Resent-Sender:', 'Return-Path:', \
                     'Sep', 'Subject:', 'To:', 'URL:', 'User-Agent:', 'X-Accept-Language:', 'X-Apparently-To:', 'X-Beenthere:X-Mailman-Version:', \
                     'X-Bulkmail:', 'X-Egroups-Return:', 'X-Keywords', 'X-Mimeole:', 'X-Pyzor:', 'X-Sender:', 'X-Spam-Level:', 'X-Spam-Status:', \
                     'X-Yahoo-Profile:', 'arial', 'cc', 'debian', 'edt', 'esmtp', 'exmh', 'font-family:', 'font-size:', 'font-weight:', 'freshrpms', 'fri', 'gmt', \
                     'helvetica', 'html', 'ist', 'localhost', 'message-id', 'mon', 'mv', 'nbsp', 'pdt', 'perl', 'pgp', 'qmail', 'rpm', 'sans-serif', 'sat', \
                     'single-drop', 'smtp', 'spambayes', 'sun', 'thu', 'tue', 'unix', 'verdana', 'wed', 'x-beenthere', 'x-mailer', 'x-mailscanner', \
                     'x-originalarrivaltime:', 'x-priority', 'x-status', 'x-uid', 'xml'])
                            
 
        # If token contains any of these - ignore it.
        self.remove = set(['!', '\\', '/', ',', '.', '@', '=', '[', ']', '(', ')', ':', ';', '?', '^', '{', '}', '|', '<', '>', '"', '#', '%', '&', '+', '`', '~', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9'])

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
            '''if flag:
                if token == 'Subject:':
                    flag = False
                continue
            '''
            # Remove HTML tags and URLs
            if self.checkUnwanted(token) == False or ('<' in token or '>' in token) or token.startswith('http://'):
                #print token
                continue

            #    for entry in self.splitOnPunctuations(token, regex):
            token = str.lower(str.lstrip(str.rstrip(token, string.punctuation), string.punctuation))
            if self.toConsiderOrNotToConsider(token):
                    tokens.append(token)
        return tokens

    # Counts w|c for both bernoulli and multinomial; total number of words in a document
    def countWordsInDocument(self, wordFreqMultinomial, wordFreqBernoulli, document):
        flag = set() # Keeps track of word that has already been counted once for a particular document - For Bernoulli Model
        count = 0 # Counts total number of words in document
        for entry in self.fetchTokens(document):
            count += 1
            self.allWordsInCorpus.add(entry)
            wordFreqMultinomial[entry] += 1
            if entry in flag:
                continue
            wordFreqBernoulli[entry] += 1
            flag.add(entry)
        return count

    def creatingVector(self, wordFreqMultinomial, wordFreqBernoulli, classType):
        docCount = 0 # Total spam/non spam documents in training data
        wordCount = 0 # Count of words in class
        # Reading all files in train directory
        directoryPath = self.directory + '/train/' + classType
        for fileName in os.listdir(directoryPath):
            with open(directoryPath + '/' + fileName) as document:
                wordCount += self.countWordsInDocument(wordFreqMultinomial, wordFreqBernoulli, document)
                docCount += 1
            #print "File: ", fileName
            #for entry in wordCountInDocs:
            #    print entry, wordCountInDocs[entry]
        return docCount, wordCount

    def increaseCountForWords(self, count):
        for entry in count:
            count[entry] += 1
    
    # Adds words missing in class2 but present in class1, to class2 with count 0 
    def addWord(self, count1, count2):
        count1keys = count1.elements()
        count2keys = count2.elements()
        for entry in count1keys:
            if entry not in count2keys:
                count2[entry] = 0 
        #print "BEFORE: ", count2
        #self.increaseCountForWords(count2) #Adding 1 to all counts
        #print "AFTER: ", count2

    def smoothCounts(self, wordCountInSpam_Multinomial, wordCountInNotSpam_Multinomial, wordCountInSpam_Bernoulli, wordCountInNotSpam_Bernoulli):
        print "Smoothing word counts..."
        self.addWord(wordCountInNotSpam_Multinomial, wordCountInSpam_Multinomial)
        self.addWord(wordCountInSpam_Multinomial, wordCountInNotSpam_Multinomial)
        
        self.addWord(wordCountInNotSpam_Bernoulli, wordCountInSpam_Bernoulli)
        self.addWord(wordCountInSpam_Bernoulli, wordCountInNotSpam_Bernoulli)
        
        self.increaseCountForWords(wordCountInSpam_Bernoulli)
        self.increaseCountForWords(wordCountInNotSpam_Bernoulli)
        
        self.increaseCountForWords(wordCountInSpam_Multinomial)
        self.increaseCountForWords(wordCountInNotSpam_Multinomial)
        #print wordCountInSpam_Bernoulli
        #print wordCountInNotSpam_Bernoulli
        #print wordCountInSpam_Multinomial
        #print wordCountInNotSpam_Multinomial
   
        
    # Removing words with frequency lower than 5 from consideration
    def deleteWordUpdateCount(self, entry):
        # Delete word from allWordsInCorpus
        self.allWordsInCorpus.discard(entry)

        #Update Spam Word Count
        self.totWordsInSpam -= self.wordCountInSpam_Multinomial[entry]
        # remove entry from Bernoulli and Multinomial
        del self.wordCountInSpam_Multinomial[entry]
        del self.wordCountInSpam_Bernoulli[entry]
       
        # Same steps for not spam docs 
        self.totWordsInNotSpam -= self.wordCountInNotSpam_Multinomial[entry]
        del self.wordCountInNotSpam_Multinomial[entry]
        del self.wordCountInNotSpam_Bernoulli[entry]

    # If from the initial Count of the words in spam/ non spam document - the count is less than 10 remove them.
    # And update both multinomial and bernoulli counters + the word counts
    def lowFrequency(self):
        for entry in list(self.allWordsInCorpus):
            if self.wordCountInNotSpam_Multinomial[entry] + self.wordCountInSpam_Multinomial[entry] < 10:
                self.deleteWordUpdateCount(entry)
         
    def removeWordsFromConsideration(self):
        self.lowFrequency()
        #self.removeNumbers()

    def calculate(self):
        print "Reading Files..."
        self.totNotSpamDocs, self.totWordsInNotSpam = self.creatingVector(self.wordCountInNotSpam_Multinomial, self.wordCountInNotSpam_Bernoulli, 'notspam')
        self.totSpamDocs, self.totWordsInSpam = self.creatingVector(self.wordCountInSpam_Multinomial, self.wordCountInSpam_Bernoulli, 'spam')
        self.removeWordsFromConsideration()
        
        # + 2 for smoothing
        self.totSpamDocs += 2
        self.totNotSpamDocs += 2
        self.totTrainingDocs = self.totNotSpamDocs + self.totSpamDocs
        
        self.smoothCounts(self.wordCountInNotSpam_Multinomial, self.wordCountInSpam_Multinomial, self.wordCountInSpam_Bernoulli, self.wordCountInNotSpam_Bernoulli)

    def getWordsInDocument(self, document):
        documentDict = Counter()
        for entry in self.fetchTokens(document):
            documentDict[entry] += 1
        return documentDict

    def getWordsInAllDocuments(self, documentDictList, classType):
        # Reading all files in train directory
        directoryPath = self.directory + '/train/' + classType
        for fileName in os.listdir(directoryPath):
            with open(directoryPath + '/' + fileName) as document:
                documentDictList.append(self.getWordsInDocument(document))

