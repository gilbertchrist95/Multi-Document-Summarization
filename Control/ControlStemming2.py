from Entity.KamusKataDasar import KamusKataDasar
import re


class ControlStemming2:
    LIST_ROOT_WORD=[]

    def __init__(self):
        self.rootWord = KamusKataDasar()
        var = self.rootWord.read()
        self.LIST_ROOT_WORD=var.split()

    def setKata(self,kata):
        self.kata = kata
        self.akarKata = kata
        bersikan = ''

    def isRootword(self, token):
        if token in self.LIST_ROOT_WORD:
            return True
        else:
            return False

    def doStemming(self,kata):
        self.setKata(kata)
        if len(kata)<=3:
            return kata
        elif self.isRootword(kata):
            return kata
        else:
            self.hapusInfelksionalSuffiks()
            self.hapusDerivationSuffiks()

    def hapusInfelksionalSuffiks(self):
        pass

    def hapusDerivationSuffiks(self):
        isHapusSuffix = False
