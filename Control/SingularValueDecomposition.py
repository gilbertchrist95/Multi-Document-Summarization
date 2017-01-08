import sys

from math import *

class SingularValueDecomposition:
    def __init__(self, matrix):
        self.A=matrix
        self.m = len(self.A)
        self.n = len(self.A[0])

        self.nu = min(self.m,self.n)

        self.S = [0 for i in range(min(self.m+1,self.n))]
        self.U = [[0 for i in range(self.nu)] for j in range(self.m)]
        self.V = [[0 for i in range(self.n)] for j in range(self.n)]

        self.e = [0 for i in range(self.n)]
        self.work = [0 for i in range(self.m)]

        self.wantU = True
        self.wantV = True

        self.nct = min(self.m - 1, self.n)
        self.nrt = max(0, (min(self.n - 2, self.m)))
        self.hitung()


    def hitung(self):
        for k in range(0, max(self.nct, self.nrt)):
            if k < self.nct:
                self.S[k] = 0
                for i in range(k, self.m):
                    self.S[k] = hypot(self.S[k], self.A[i][k])
                if self.S[k] != 0.0:
                    if self.A[k][k] < 0.0:
                        self.S[k] = -(self.S[k])
                    for i in range(k, self.m):
                        self.A[i][k] /= self.S[k]
                    self.A[k][k] += 1
                self.S[k] = -(self.S[k])

            for j in range(k + 1, self.n):
                if k < self.nct and self.S[k] != 0:
                    t = 0
                    for i in range(k, self.m):
                        t += self.A[i][k] * self.A[i][j]
                    t = -t / self.A[k][k]
                    for i in range(k, self.m):
                        self.A[i][j] += t * self.A[i][k]
                self.e[j] = self.A[k][j]

            if self.wantU and (k < self.nct):
                for i in range(k, self.m):
                    self.U[i][k] = self.A[i][k]

            if k < self.nrt:
                self.e[k] = 0
                for i in range(k + 1, self.n):
                    self.e[k] = hypot(self.e[k], self.e[i])
                if self.e[k] != 0.0:
                    if self.e[k + 1] < 0.0:
                        self.e[k] = -(self.e[k])
                    for i in range(k + 1, self.n):
                        self.e[i] /= self.e[k]
                    self.e[k + 1] += 1.0
                self.e[k] = -self.e[k]
                if ((k + 1) < self.m) and self.e[k] != 0.0:
                    for i in range(k + 1, self.m):
                        self.work[i] = 0.0
                    for j in range(k + 1, self.n):
                        for i in range(k + 1, self.m):
                            self.work[i] += self.e[j] * self.A[i][j]
                    for j in range(k + 1, self.n):
                        t = -self.e[j] / self.e[k + 1]
                        for i in range(k + 1, self.m):
                            self.A[i][j] += t * self.work[i]
                if self.wantV:
                    for i in range(k + 1, self.n):
                        self.V[i][k] = self.e[i]

        p = min(self.n, self.m + 1)
        if self.nct < self.n:
            self.S[self.nct] = self.A[self.nct][self.nct]
        if self.m < p:
            self.S[p - 1] = 0.0
        if self.nrt + 1 < p:
            self.e[self.nrt] = self.A[self.nrt][p - 1]
        self.e[p - 1] = 0.0

        if self.wantU:
            for j in range(self.nct, self.nu):
                for i in range(0, self.m):
                    self.U[i][j] = 0.0
                self.U[j][j] = 1.0
            for k in range(self.nct - 1, -1, -1):
                if self.S[k] != 0.0:
                    for j in range(k + 1, self.nu):
                        t = 0
                        for i in range(k, self.m):
                            t += self.U[i][k] * self.U[i][j]
                        t = -t / self.U[k][k]
                        for i in range(k, self.m):
                            self.U[i][j] += t * self.U[i][k]
                    for i in range(k, self.m):
                        self.U[i][k] = -(self.U[i][k])
                    self.U[k][k] = 1.0 + self.U[k][k]
                    for i in range(0, k - 1):
                        self.U[i][k] = 0.0
                else:
                    for i in range(0, self.m):
                        self.U[i][k] = 0.0
                    self.U[k][k] = 1.0

        if self.wantV:
            for k in range(self.n - 1, -1, -1):
                if (k < self.nrt) and (self.e[k] != 0.0):
                    for j in range(k + 1, self.nu):
                        t = 0
                        for i in range(k + 1, self.n):
                            t += self.V[i][k] * self.V[i][j]
                        t = -t / self.V[k + 1][k]
                        for i in range(k + 1, self.n):
                            self.V[i][j] += t * self.V[i][k]
                for i in range(0, self.n):
                    self.V[i][k] = 0.0
                self.V[k][k] = 1.0

        # // Main         iteration         loop        for the singular values.
        pp = p - 1
        iter = 0
        eps = pow(2.0, -52.0)
        tiny = pow(2.0, -966.0)

        while p > 0:

            for k in range(p - 2, -2, -1):
                if k == -1:
                    break
                if (abs(self.e[k]) <= tiny + eps * (abs(self.S[k]) + abs(self.S[k + 1]))):
                    self.e[k] = 0.0
                    break
            if k == p - 2:
                kase = 4
            else:
                for ks in range(p - 1, k - 1, -1):
                    if (ks == k):
                        break
                    t = 0
                    if (ks != p):
                        t = abs(self.e[ks])
                    if ks != k + 1:
                        t += abs(self.e[ks - 1])
                    if abs(self.S[ks]) <= tiny + eps * t:
                        self.S[ks] = 0.0
                        break
                if ks == k:
                    kase = 3
                elif ks == p - 1:
                    kase = 1
                else:
                    kase = 2
                    k = ks
            k += 1

            if kase == 1:
                f = self.e[p - 2]
                self.e[p - 2] = 0.0
                for j in range(p - 2, k - 1, -1):
                    t = hypot(self.S[j], f)
                    cs = self.S[j] / t
                    sn = f / t
                    self.S[j] = t
                    if j != k:
                        f = -sn * self.e[j - 1]
                        self.e[j - 1] = cs * self.e[j - 1]
                    if self.wantV:
                        for i in range(0, self.n):
                            t = cs * self.V[i][j] + sn * self.V[i][p - 1]
                            self.V[i][p - 1] = -sn * self.V[i][j] + cs * self.V[i][p - 1]
                            self.V[i][j] = t
            elif kase == 2:
                f = self.e[k - 1]
                self.e[k - 1] = 0.0
                for j in range(k, p):
                    t = hypot(self.S[j], f)
                    cs = self.S[j] / t
                    sn = f / t
                    self.S[j] = t
                    f = -sn * self.e[j]
                    self.e[j] = cs * self.e[j]
                    if self.wantU:
                        for i in range(0, self.m):
                            t = cs * self.U[i][j] + sn * self.U[i][k - 1]
                            self.U[i][k - 1] = -sn * self.U[i][j] + cs * self.U[i][k - 1]
                            self.U[i][j] = t
            elif kase == 3:
                scale = max(max(max(max(abs(self.S[p - 1]), abs(self.S[p - 2])), abs(self.e[p - 2])),
                                abs(self.S[k])), abs(self.e[k]))
                sp = self.S[p - 1] / scale
                spm1 = self.S[p - 2] / scale
                epm1 = self.e[p - 2] / scale
                sk = self.S[k] / scale
                ek = self.e[k] / scale
                b = ((spm1 + sp) * (spm1 - sp) + epm1 * epm1) / 2.0
                c = (sp * epm1) * (sp * epm1)
                shift = 0.0
                if (b != 0.0) or (c != 0.0):
                    shift = sqrt(b * b + c)
                    if b < 0.0:
                        shift = -shift
                    shift = c / (b + shift)
                f = (sk + sp) * (sk - sp) + shift
                g = sk * ek

                for j in range(k, p - 1):
                    t = hypot(f, g)
                    cs = f / t
                    sn = g / t
                    if j != k:
                        self.e[j - 1] = t
                    f = cs * self.S[j] + sn * self.e[j]
                    self.e[j] = cs * self.e[j] - sn * self.S[j]
                    g = sn * self.S[j + 1]
                    self.S[j + 1] = cs * self.S[j + 1]
                    if self.wantV:
                        for i in range(0, self.n):
                            t = cs * self.V[i][j] + sn * self.V[i][j + 1]
                            self.V[i][j + 1] = -sn * self.V[i][j] + cs * self.V[i][j + 1]
                            self.V[i][j] = t
                    t = hypot(f, g)
                    cs = f / t
                    sn = g / t
                    self.S[j] = t
                    f = cs * self.e[j] + sn * self.S[j + 1]
                    self.S[j + 1] = -sn * self.e[j] + cs * self.S[j + 1]
                    g = sn * self.e[j + 1]
                    self.e[j + 1] = cs * self.e[j + 1]
                    if self.wantU and j < self.m - 1:
                        for i in range(0, self.m):
                            t = cs * self.U[i][j] + sn * self.U[i][j + 1]
                            self.U[i][j + 1] = -sn * self.U[i][j] + cs * self.U[i][j + 1]
                            self.U[i][j] = t
                self.e[p - 2] = f
                iter = iter + 1

            elif kase == 4:
                if self.S[k] <= 0.0:
                    if self.S[k] < 0.0:
                        self.S[k] = -self.S[k]
                    else:
                        self.S[k] = 0.0
                    if self.wantV:
                        for i in range(0, pp + 1):
                            self.V[i][k] = -(self.V[i][k])
                while k < pp:
                    if self.S[k] >= self.S[k + 1]:
                        break
                    t = self.S[k]
                    self.S[k] = self.S[k + 1]
                    self.S[k + 1] = t
                    if self.wantV and k < self.n - 1:
                        for i in range(0, self.n):
                            t = self.V[i][k + 1]
                            self.V[i][k + 1] = self.V[i][k]
                            self.V[i][k] = t
                    if self.wantU and k < self.m - 1:
                        for i in range(0, self.m):
                            t = self.U[i][k + 1]
                            self.U[i][k + 1] = self.U[i][k]
                            self.U[i][k] = t
                    k += 1
                iter = 0
                p -= 1

    def getS(self):
        return self.S

    def getU(self):
        return self.U

    def getV(self):
        return self.V


x = [[0 for i in range(3)] for j in range(4)]
x[0] = [1, 0,1]
x[1] = [1, 1,1]
x[2] = [1, 1,1]
x[3] = [0, 1,1]
svd = SingularValueDecomposition(x)
print(svd.getS())
print(svd.getU())
print(svd.getV())

