class Preprocessing:
    def __init__(self):
        self.preprocessing = []
        self.dokumen = []

    def setDokumen(self,dokumen):
        self.dokumen = dokumen

    def getDokumen(self):
        return self.dokumen

    def setPreprocessingResult(self,dokumen):
        self.preprocessing = dokumen

    def getPreprocessingResult(self):
        return self.preprocessing