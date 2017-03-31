from math import *


class SingularValueDecomposition:
    def __init__(self, matrix):
        self.A = self.U = matrix
        self.m = len(self.A)
        self.n = len(self.A[0])

        self.V = [x[:] for x in [[0] * self.n] * self.n]
        self.e = [0] * self.n

    def pythag(self, a, b):
        absa = abs(a)
        absb = abs(b)
        if (absa > absb):
            return absa * sqrt(1 + pow(absb / absa, 2))
        else:
            if absb == 0.0:
                return 0.0
            else:
                return absb * sqrt(1 + pow(absa / absb, 2))

    def count(self):
        # flag = False
        m = len(self.A)
        n = len(self.A[0])
        eps = pow(2.0, -52.0)
        g = x = 0
        for i in range(0, n):
            self.e[i] = g
            s = 0
            l = i+1
            for j in range (i,m): s+=pow(self.U[j][i],2)
