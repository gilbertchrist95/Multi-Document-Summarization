
class Dokumen:
    def __init__(self):
        self.dokumen = []
        self.summaries = {}

    def setDokumen(self, dokumen):
        self.dokumen = dokumen

    def getDokumen(self):
        return self.dokumen

    def clear(self):
        self.dokumen.clear()

    def setSummaries(self, summaries):
        self.summaries = summaries

    def getSummaries(self):
        return self.summaries




