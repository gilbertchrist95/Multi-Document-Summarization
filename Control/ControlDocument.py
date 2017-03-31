import os
from Entity.EntityDocument import EntityDokumen


class ControlDokumen:
    def __init__(self):
        self.dokumen = EntityDokumen()

    def saveDocument(self, folderPath):
        dokumen = []
        self.listFile = os.listdir(folderPath)
        for list in self.listFile:
            # print(list)
            if list[-3:] == 'txt':
                addressFile = str(folderPath + "/" + list)
                File = open(addressFile, 'r')
                isiDokumen = File.read()
                dokumen.append([isiDokumen])
        self.dokumen.setDocument(dokumen)

    def getDocument(self):
        return self.dokumen.getDocument()

    def resetDocument(self):
        self.dokumen.clear()

    def saveSummaries(self, folderPath):
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

    def getSummaries(self):
        return self.dokumen.getSummaries()