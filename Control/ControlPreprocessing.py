from Entity.EntityPreprocessing import EntityPreprocessing
from Control.ControlStemming import ControlStemming
from Control.ControlFiltering import ControlFiltering

import re


class ControlPreprocessing():
    documentPreprocessing = []
    document = []

    def __init__(self):
        # super(self.__class__, self).__init__()
        self.controlFiltering = ControlFiltering()
        self.preprocessing = EntityPreprocessing()
        self.controlStemming = ControlStemming()

    def doPreprocessing(self, document):
        self.documentPreprocessing.clear()
        self.document.clear()
        self.documentPreprocessing = document
        n = len(self.documentPreprocessing)
        for i in range(n):
            self.segmentationSentences(i)
            self.caseFolding(i)
            self.tokenizing(i)
            self.filtering(i)
            self.stemming(i)
            self.documentPreprocessing[i] = list(filter(None, self.documentPreprocessing[i]))
        dokumen = []
        dokumenProcessing = []
        maximumSentence = max(len(l) for l in self.documentPreprocessing)

        for i in range(maximumSentence):
            for l in self.document:
                if not l == []:
                    dokumen.append(l.pop(0))
            for k in self.documentPreprocessing:
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
        pattern = re.compile("[.?!]")
        listSentences = (re.split(pattern, self.documentPreprocessing[i][0]))
        listSentences.pop()
        self.documentPreprocessing[i] = [sentence.strip() for sentence in listSentences]  # strip list empty sentence
        self.document.append(self.documentPreprocessing[i])

    def caseFolding(self, i):
        delimiter = "\"", "\'", "{", "“", "”", "}", "(", ")", "[", "]", ">", "<", "_", "-", "=", "+", "|", "\\", ":", ",", ";", "/", "~", "@", "#", "$", "%", "^", "&", "*", "\r", "\n", "\t", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"
        regexPattern = '|'.join(map(re.escape, delimiter))
        self.documentPreprocessing[i] = [re.split(regexPattern, kalimat.lower()) for kalimat in
                                         self.documentPreprocessing[i]]

    def tokenizing(self, i):
        self.documentPreprocessing[i] = [' '.join(list).split() for list in self.documentPreprocessing[i]]

    def filtering(self, i):
        self.documentPreprocessing[i] = self.controlFiltering.doFiltering(self.documentPreprocessing[i])

    def stemming(self, i):
        n = len(self.documentPreprocessing[i])
        for j in range(0, n):
            self.documentPreprocessing[i][j] = self.controlStemming.doStemming(token=self.documentPreprocessing[i][j])

    def getSentencesDocument(self):
        return self.preprocessing.getDokumen()

    def getResultPreprocessing(self):
        return self.preprocessing.getPreprocessingResult()
