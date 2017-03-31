from numpy import *

class SingularValueDecomposition:
    # def __init__(self):


    def count(self, matrix):
        self.matriks = array(matrix)
        self.U = []
        self.S = []
        self.Vt = []
        self.U, self.S, self.Vt = linalg.svd(self.matriks, full_matrices=False)

    def getU(self):
        return self.U.tolist()

    def getS(self):
        return self.S.tolist()

    def getVt(self):
        return self.Vt.tolist()
