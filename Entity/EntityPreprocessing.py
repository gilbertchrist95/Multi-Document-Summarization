class EntityPreprocessing:
    def __init__(self):
        self.preprocessing = []
        self.document = []

    def setDocument(self, document):
        self.document = document

    def getDokumen(self):
        return self.document

    def setPreprocessingResult(self, preprocessing):
        self.preprocessing = preprocessing

    def getPreprocessingResult(self):
        return self.preprocessing