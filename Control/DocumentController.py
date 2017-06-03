import os
from Entity.EntityDocument import EntityDokumen

class DocumentController:
    def __init__(self):
        self.dokumen = EntityDokumen()

    def saveDocument(self, folderPath):
        dokumen = []
        self.listFile = os.listdir(folderPath)
        for list in self.listFile:
            if list[-3:] == 'txt': #cek 3 karater dri blakang
                addressFile = str(folderPath + "/" + list)
                File = open(addressFile, 'r')
                isiDokumen = File.read()
                dokumen.append([isiDokumen])
        self.dokumen.setDocument(dokumen) #dalam list

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
