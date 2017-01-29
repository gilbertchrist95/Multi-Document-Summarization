from Entity.KamusStopword import KamusStopWord


class ControlFiltering:
    def __init__(self):
        kamus = KamusStopWord()
        var = kamus.read()
        self.LIST_STOP_WORD = var.split()

    def doFiltering(self, documentPreprocessing):
        for j in range(len(documentPreprocessing)):
            documentPreprocessing[j] = list(
                token for token in documentPreprocessing[j] if token not in self.LIST_STOP_WORD)
        return documentPreprocessing
