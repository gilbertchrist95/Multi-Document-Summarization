import os
from Entity.EntityDocument import Dokumen


class ControlDokumen:
    def __init__(self):
        self.dokumen = Dokumen()

    def saveDocument(self, folderPath):
        # self.folderPath = folderPath
        dokumen = []
        self.listFile = os.listdir(folderPath)
        for list in self.listFile:
            if list[-3:] == 'txt':
                # print(list)
                addressFile = str(folderPath + "/" + list)
                File = open(addressFile, 'r')
                # print(sumber)
                isiDokumen = File.read()
                dokumen.append([isiDokumen])
        self.dokumen.setDokumen(dokumen)

    def getDocument(self):
        return self.dokumen.getDokumen()

    def resetDocument(self):
        self.dokumen.clear()

    def saveSummarization(self, folderPath):
        summaries = {}
        listSummary = os.listdir(folderPath)
        for listS in listSummary:
            sumberJudul = listS.split('-')
            sumber = sumberJudul[0]
            addressFile = str(folderPath + "/" + listS)
            File = open(addressFile, 'r')
            isiRingkasan = File.read()
            summaries[sumber] = isiRingkasan
        self.dokumen.setSummaries(summaries)

    def getSummary(self):
        return self.dokumen.getSummaries()