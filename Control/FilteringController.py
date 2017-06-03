from Entity.KamusStopword import KamusStopWord


class FilteringController:
    def __init__(self):
        self.kamus = KamusStopWord()
        # var = kamus.read()
        # self.LIST_STOP_WORD = var.split()

    def doFiltering(self, documentPreprocessing): #dP = kalimat yg di belah
        LIST_STOP_WORD = self.kamus.read()
        documentPreprocessing = list(
            token for token in documentPreprocessing if token not in LIST_STOP_WORD)
        return documentPreprocessing

    # def doFiltering(self, documentPreprocessing):
    #     for j in range(len(documentPreprocessing)):
    #         documentPreprocessing[j] = list(
    #             token for token in documentPreprocessing[j] if token not in self.LIST_STOP_WORD)
    #     return documentPreprocessing
