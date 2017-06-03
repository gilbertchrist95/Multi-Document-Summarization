from Entity.EntityPreprocessor import EntityPreprocessor
from Control.StemmingController import StemmingController
from Control.FilteringController import FilteringController

import re


class PreprocessorController:
    documentPreprocessing = []
    document = []

    def __init__(self):
        # super(self.__class__, self).__init__()
        self.controlFiltering = FilteringController()
        self.preprocessing = EntityPreprocessor()
        self.controlStemming = StemmingController()

    def doPreprocessing(self, document):
        self.documentPreprocessing.clear()
        self.document.clear()
        self.documentPreprocessing = document #list of list

        n = len(self.documentPreprocessing)
        for i in range(n):
            self.segmentationSentences(i)
            self.caseFolding(i)
            self.tokenizing(i)
            self.filtering(i)
            self.stemming(i)
            self.documentPreprocessing[i] = list(filter(None, self.documentPreprocessing[i])) #filter yg None
        dokumen = []
        dokumenProcessing = []
        maximumSentence = max(len(l) for l in self.documentPreprocessing)

        for i in range(maximumSentence): #ngapo make ini
            for l in self.document: #length dokumen kan beda beda.. jadi yo mak itula
                # print(l)
                if not l == []:
                    dokumen.append(l.pop(0))
            for k in self.documentPreprocessing:
                # print(k)
                if not k == []:
                    dokumenProcessing.append(k.pop(0))

        if len(dokumenProcessing) != len(dokumen):
            print(maximumSentence)
            print(len(dokumen))
            print('something wrong')
            exit

        self.preprocessing.setDocument(dokumen)
        self.preprocessing.setPreprocessingResult(dokumenProcessing)

    def segmentationSentences(self, i):
        pattern = re.compile("[.?!]") #compile !.?
        listSentences = (re.split(pattern, self.documentPreprocessing[i][0])) #string of list
        listSentences.pop() #selalu ad string kosong
        self.documentPreprocessing[i] = [sentence.strip() for sentence in listSentences]  # strip list empty sentence
        # print(self.documentPreprocessing[i])
        self.document.append(self.documentPreprocessing[i]) #list of list

    def caseFolding(self, i):
        delimiter = "\"", "\'", "{", "“", "”", "}", "(", ")", "[", "]", ">", "<", "_", "-", "=", "+", "|", "\\", ":", ",", ";", "/", "~", "@", "#", "$", "%", "^", "&", "*", "\r", "\n", "\t", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"
        regexPattern = '|'.join(map(re.escape, delimiter))#Escape all the characters in pattern except ASCII letters, numbers and '_'.
        self.documentPreprocessing[i] = [re.split(regexPattern, kalimat.lower()) for kalimat in
                                         self.documentPreprocessing[i]]

    def tokenizing(self, i):
        self.documentPreprocessing[i] = [' '.join(list).split() for list in self.documentPreprocessing[i]]
        #split by space and then ' ' was joined

    def filtering(self, i):
        n = len(self.documentPreprocessing[i])
        for j in range(0, n): #perkalimat
            self.documentPreprocessing[i][j] = self.controlFiltering.doFiltering(self.documentPreprocessing[i][j])

    def stemming(self, i):
        n = len(self.documentPreprocessing[i])
        for j in range(0, n):
            # print(self.documentPreprocessing[i][j])
            self.documentPreprocessing[i][j] = self.controlStemming.doStemming(token=self.documentPreprocessing[i][j])

    def getSentencesDocument(self):
        return self.preprocessing.getDokumen()

    def getResultPreprocessing(self):
        return self.preprocessing.getPreprocessingResult()
