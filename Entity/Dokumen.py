
class Dokumen:
    def __init__(self):
        self.dokumen = {}

    def setDokumen(self, sumber, judul, isi):
        self.dokumen[sumber]=[judul, isi]

    def getSumber(self):
        return list(self.dokumen.keys())

    def getJudul(self,sumber):
        return str(self.dokumen[sumber][0])

    def getIsi (self,sumber):
        return str(self.dokumen[sumber][1])





