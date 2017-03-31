
class EntityDokumen:
    def __init__(self):
        self.document = []
        self.summaries = {}

    def setDocument(self, document):
        self.document = document

    def getDocument(self):
        return self.document

    def clear(self):
        self.document.clear()

    def setSummaries(self, summaries):
        self.summaries = summaries

    def getSummaries(self):
        return self.summaries




