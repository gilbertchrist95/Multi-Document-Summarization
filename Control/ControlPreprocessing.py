from Entity.EntityPreprocessing import Preprocessing
from Control.ControlStemming import ControlStemming
from Control.ControlFiltering import ControlFiltering

import re


class ControlPreprocessing(ControlStemming):
    documentPreprocessing = []
    document = []

    def __init__(self):
        super(self.__class__, self).__init__()

        self.controlFiltering = ControlFiltering()
        self.preprocessing = Preprocessing()
        self.controlStemming = ControlStemming()

    def doPreprocessing(self, document):  # dokumen awal harus sudah jadi list,
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
            print(len(self.document[i]) == len(self.documentPreprocessing[i]))

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

        self.preprocessing.setDokumen(dokumen)
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
        self.documentPreprocessing[i]= self.controlFiltering.doFiltering(self.documentPreprocessing[i])
        # var = self.kamus.read()
        # LIST_STOP_WORD = var.split()
        # n = self.documentPreprocessing[i].__len__()
        # for j in range(0, n):
        #     self.documentPreprocessing[i][j] = (
        #         list(token for token in self.documentPreprocessing[i][j] if token not in LIST_STOP_WORD))

    def stemming(self, i):
        for j in range(len(self.documentPreprocessing[i])):
            self.documentPreprocessing[i][j] = self.controlStemming.stemming(kalimat=self.documentPreprocessing[i][j])
        # n = self.documentPreprocessing[i].__len__()
        # for j in range(0, n):
        #     self.documentPreprocessing[i][j] = ControlStemming.stemming(self, kalimat=self.documentPreprocessing[i][j])

    def getSentencesDocument(self):
        return self.preprocessing.getDokumen()

    def getPreprocessing(self):
        return self.preprocessing.getPreprocessingResult()



        # def segmentationSentences(self):
        #     # print(self.dokumen.keys())
        #     # j=1
        #     pattern = re.compile("[.?!]")
        #     for doc in self.dokumen:
        #         isi = str(self.dokumen[doc][1])
        #         segmen=re.split(pattern, isi)
        #         segmen.pop()
        #         self.newDocument[doc]=segmen

        # def caseFolding(self):
        #     for doc in self.newDocument:
        #         isi = self.newDocument[doc]
        #         self.newDocument[doc]= [kalimat.lower() for kalimat in isi]
        #         print(self.newDocument[doc])

        # def tokenizing(self):
        #     for doc in self.newDocument:
        #         list =[]
        #         isiBerita = (self.newDocument[doc])
        #         for kalimat in isiBerita:
        #             list.append(kalimat.split())
        #         self.newDocument[doc]=list

        # def filtering(self):
