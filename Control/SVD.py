from math import *


class SingularValueDecomposition:
    def __init__(self, matrix):
        self.A = self.U = matrix
        self.m = len(self.A)
        self.n = len(self.A[0])

        self.V = [x[:] for x in [[0] * self.n] * self.n]
        self.W = [0] * self.n

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
        eps = pow(2.0, -52.0)
        # its = l = nm = 0
        # anorm= c= f= g= h= s= scale= x= y= z=0.0
        rv1 = [0] * self.n
        g = scale = anorm = 0.0
        for i in range(0, self.n):
            l = i + 2
            rv1[i] = scale * g
            g = s = scale = 0.0
            if (i < self.m):
                for k in range(i, self.m): scale += abs(self.U[k][i])
                if scale != 0.0:
                    for k in range(i, self.m):
                        self.U[k][i] /= scale
                        s += pow(self.U[k][i], 2)
                    f = self.U[i][i]
                    if (f < 0):
                        g = sqrt(s)
                    else:
                        g = -sqrt(s)
                    h = f * g - s
                    self.U[i][i] = f - g
                    for j in range(l - 1, self.n):
                        s = 0
                        for k in range(i, self.m):
                            s += self.U[k][i]*self.U[k][j]
                        f = s / h
                        for k in range(i, self.m):
                            self.U[k][j] += f * self.U[k][i]
                    for k in range(i, self.m): self.U[k][i] *= scale
            self.W[i] = scale * g
            g = s = scale = 0.0
            if (i + 1 <= self.m and i + 1 != self.n):
                for k in range(l - 1, self.n): scale += abs(self.U[i][k])
                if scale != 0.0:
                    for k in range(l - 1, self.n):
                        self.U[i][k] /= scale
                        s += pow(self.U[i][k], 2)
                    f = self.U[i][l - 1]
                    if f < 0:
                        g = sqrt(s)
                    else:
                        g = -sqrt(s)
                    h = f * g - s
                    self.U[i][l - 1] = f - g
                    for k in range(l - 1, self.n): rv1[k] = self.U[i][k] / h
                    for j in range(l - 1, self.m):
                        s = 0
                        for k in range(l - 1, self.n): s += self.U[j][k] * self.U[i][k]
                        for k in range(l - 1, self.n): self.U[j][k] += s * rv1[k]
                    for k in range(l - 1, self.n): self.U[i][k] *= scale
            anorm = max(anorm, (abs(self.W[i]) + abs(rv1[i])))

        for i in range(self.n-1, -1, -1):
            if (i < self.n - 1):
                if (g != 0.0):
                    for j in range(l, self.n):
                        self.V[j][i] = (self.U[i][j] / self.U[i][l]) / g
                    for j in range(l, self.n):
                        s = 0.0
                        for k in range(l, self.n): s += self.U[i][k] * self.V[k][j]
                        for k in range(l, self.n): self.V[k][j] += s * self.V[k][i]
                for j in range(l, self.n):
                    self.V[i][j] = self.V[j][i] = 0.0
            self.V[i][i] = 1
            g = rv1[i]
            l = i

        for i in range(min(self.m, self.n)-1, -1, -1):
            l = i + 1
            g = self.W[i]
            for j in range(l, self.n): self.U[i][j] = 0.0
            if g != 0.0:
                g = 1 / g
                for j in range(l, self.n):
                    s = 0
                    for k in range(l, self.m): s += self.U[k][i] * self.U[k][j]
                    f = (s / self.U[i][i]) * g
                    for k in range(i, self.m): self.U[k][j] += f * self.U[k][i]
                for j in range(i, self.m): self.U[j][i] *= g
            else:
                for j in range(i, self.m): self.U[j][i] = 0.0
            self.U[i][i] += 1

        for k in range(self.n - 1, -1, -1):
            for its in range(0, 30):
                flag = True
                for l in range(k, -1, -1):
                    nm = l - 1
                    if l == 0 or abs(rv1[l]) <= eps * anorm:
                        flag = False
                        break
                    if (abs(self.W[nm]) <= eps * anorm): break
                if flag:
                    c = 0.0
                    s = 1.0
                    for i in range(l, k + 1):
                        f = s * rv1[i]
                        rv1[i] = c * rv1[i]
                        if abs(f) <= eps * anorm: break
                        g = self.W[i]
                        h = self.pythag(f, g)
                        self.W[i] = h
                        h = 1 / h
                        c = g * h
                        s = -f * h
                        for j in range(0, self.m):
                            y = self.U[j][nm]
                            z = self.U[j][i]
                            self.U[j][nm] = y * c + z * s
                            self.U[j][i] = z * c - y * s
                z = self.W[k]
                if (l == k):
                    if z < 0.0:
                        self.W[k] = -z
                        for j in range(0, self.n): self.V[j][k] *= -1
                    break
                if its == 29:
                    print('no convergence in 30 svdcmp iterations')
                    # break
                x = self.W[l]
                nm = k - 1
                y = self.W[nm]
                g = rv1[nm]
                h = rv1[k]
                f = ((y - z) * (y + z) + (g - h) * (g + h)) / (2 * h * y)
                g = self.pythag(f, 1.0)
                if f < 0:
                    f = ((x - z) * (x + z) + h * ((y / (f - g)) - h)) / x
                else:
                    f = ((x - z) * (x + z) + h * ((y / (f + g)) - h)) / x
                c = s = 1
                for j in range(l, nm):
                    i = j + 1
                    g = rv1[i]
                    y = self.W[i]
                    h = s * g
                    g = c * g
                    z = self.pythag(f, h)
                    rv1[j] = z
                    c = f / z
                    s = h / z
                    f = x * c + g * s
                    g = g * c - x * s
                    h = y * s
                    y *= c
                    for jj in range(0, self.n):
                        x = self.V[jj][j]
                        z = self.V[jj][i]
                        self.V[jj][j] = x * c + z * s
                        self.V[jj][i] = z * c - x * s
                    z = self.pythag(f, h)
                    self.W[j] = z
                    if z:
                        z = 1 / z
                        c = f * z
                        s = h * z
                    f = c * g + s * y
                    x = c * y - s * g
                    for jj in range(0, self.m):
                        y = self.U[jj][j]
                        z = self.U[jj][i]
                        self.U[jj][j] = y * c + z * s
                        self.U[jj][i] = z * c - y * s
                rv1[l] = 0
                rv1[k] = f
                self.W[k] = x

    def reorder(self):
        inc = 1
        su = [0]*self.m
        sv = [0]*self.n

        while inc<=self.n:
            inc*=3
            inc+=1
        while inc>1:
            inc/=3
            inc  = int(inc)
            for i in range (inc,self.n):
                sw = self.W[i]
                for k in range(0,self.m): su[k] = self.U[k][i]
                for k in range(0,self.n): sv[k] = self.V[k][i]
                j=i
                while(self.W[j-inc]<sw):
                    self.W[j]= self.W[j-inc]
                    for k in range(0, self.m): self.U[k][j]=self.U[k][j-inc]
                    for k in range(0, self.n): self.V[k][j]=self.V[k][j-inc]
                    j-=inc
                    if (j<inc):break
                self.W[j]=sw
                for k in range(0, self.m): self.U[k][j]=su[k]
                for k in range(0, self.n): self.V[k][j]=sv[k]
        for k in range(0,self.n):
            s=0
            for i in range(0,self.m):
                if self.U[i][k]<0: s+=1
            for j in range(0,self.n):
                if self.V[j][k]<0: s+=1
            if (s>(self.m+self.n)/2):
                for i in range(0, self.m): self.U[i][k] *= -1
                for j in range(0, self.n): self.V[j][k] *=-1




# x=[[1,2,3],[4,0,2],[2,1,0],[1,0,0]]
x=[[1,0],[0,1],[1,1],[2,3]]
svd = SingularValueDecomposition(x)
svd.count()
svd.reorder()

U = svd.U
S = svd.W
Vt = svd.V
Vt = [[j[i] for j in svd.V] for i in range(len(svd.V))]
US = [[0 for i in range(len(S))] for j in range(len(U))]
# # SVt = [[0 for i in range(len(Vt))] for j in range(len(S))]
USVt = [[0 for i in range(len(Vt))] for j in range(len(US))]
for i in range(len(U)):
    for j in range(len(S)):
        US[i][j] = U[i][j] * S[j]
for i in range(len(US)):
    for j in range(len(Vt[0])):
        for k in range(len(Vt)):
            USVt[i][j]+=US[i][k]*Vt[k][j]
#
for i in  USVt:
    print (i)