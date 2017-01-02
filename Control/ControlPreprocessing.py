from pip._vendor.distlib.database import new_dist_class

from Entity.Preprocessing import Preprocessing
from Control.ControlDocument import ControlDokumen
from Control.ControlStemming import ControlStemming
from Entity.KamusStopword import KamusStopWord
import re


class ControlPreprocessing(ControlStemming):
    dokumen = {}
    newDocument = {}

    def __init__(self):
        super(self.__class__, self).__init__()
        self.kamus = KamusStopWord()
        # self.doPreprocessing()
        # ControlDokumen.__init__(self)
        # self.preprocessing = Preprocessing()
        # self.controlDokumen = ControlDokumen()

    def doPreprocessing(self, dokumen):
        self.dokumen = dokumen
        for doc in self.dokumen:
            self.segmentationSentences(doc)
            # # print(self.dokumen[doc])
            self.caseFolding(doc)
            # print(self.dokumen[doc])
            self.tokenizing(doc)
            # print(self.dokumen[doc])
            self.fitering(doc)
            # print(self.dokumen[doc])
            self.stemming(doc)
            # self.tokenizing()
            # self.filtering()

    def segmentationSentences(self, doc):
        pattern = re.compile("[.?!]")
        self.dokumen[doc] = re.split(pattern, str(self.dokumen[doc][1]))

    def caseFolding(self, doc):
        delimiter = "\"", "\'", "{", "}", "(", ")", "[", "]", ">", "<", "_", "-", "=", "+", "|", "\\", ":", ",", ";", "/", "~", "@", "#", "$", "%", "^", "&", "*", "\r", "\n", "\t", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"
        regexPattern = '|'.join(map(re.escape, delimiter))
        self.dokumen[doc] = [re.split(regexPattern, kalimat.lower()) for kalimat in self.dokumen[doc]]

    def tokenizing(self, doc):
        self.dokumen[doc] = [' '.join(list).split() for list in self.dokumen[doc]]
        self.dokumen[doc].pop()

    def fitering(self, doc):
        var = self.kamus.read()
        LIST_STOP_WORD = var.split()
        n = self.dokumen[doc].__len__()
        i = 0
        while i < n:
            self.dokumen[doc][i] = (list(token for token in self.dokumen[doc][i] if token not in LIST_STOP_WORD))
            i += 1

    def stemming(self, doc):
        # ControlStemming.stemming(doc
        n = self.dokumen[doc].__len__()
        i = 0
        while i < n:
            self.dokumen[doc][i] = ControlStemming.stemming(self, kalimat=self.dokumen[doc][i])
            i += 1





            # def segmentationSentences(self):
            #     # print(self.dokumen.keys())
            #     # i=1
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
