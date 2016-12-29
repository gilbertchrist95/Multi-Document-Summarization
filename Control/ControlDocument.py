import os
from Entity.Document import Dokumen


class ControlDokumen:
    def __init__(self):
        self.dokumen = Dokumen()

    def simpan_dokumen(self,folderPath):
        self.folderPath=folderPath

        self.listFile = os.listdir(folderPath)
        for list in self.listFile:
            # print(list)
            sumberJudul = list.split('-')
            sumber = sumberJudul[0]
            judul = sumberJudul[1][:-4]
            addressFile = str(folderPath+"/"+list)
            File = open(addressFile,'r')
            isiDokumen = File.read()
            self.dokumen.setDokumen(sumber,judul,isiDokumen)

    def getBerita(self,sumber):
        return self.dokumen.getIsi(sumber)