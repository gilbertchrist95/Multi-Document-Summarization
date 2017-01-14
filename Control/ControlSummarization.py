from math import sqrt
from Control.SingularValueDecomposition import SingularValueDecomposition


class ControlSummarization:
    # dokumen = []
    # matrix = []
    # term = []
    # similarity = []

    def doSummarization(self, preprocessingResult, sentencesDocument):
        self.sentencesClustering(preprocessingResult, sentencesDocument)

    def sentencesClustering(self, preprocessingResult, sentencesDocument):
        similarity = self.latentSemancticIndexing(preprocessingResult)
        # self.similarityHistogramClustering(similarity, sentencesDocument)

    def latentSemancticIndexing(self, preprocessingResult):
        term, matrix = self.setMatrix(preprocessingResult)
        # for i in matrix:
        #     print(i)
        U, S, Vt = self.singularValueDecomposition(matrix)

        similarity = self.countSimilarity(term, preprocessingResult, U, S, Vt)

        return 0

    def setMatrix(self, preprocessingResult):
        matrix = []
        term = []
        nColumn = 0
        iColumn = 0
        for doc in preprocessingResult:
            nColumn += len(doc)
        for doc in preprocessingResult:
            for sentence in doc:
                for token in sentence:
                    if token in term:
                        matrix[term.index(token)][iColumn] += 1
                    else:
                        term.append(token)
                        matrix.append([0] * nColumn)
                        matrix[len(term) - 1][iColumn] = 1
                iColumn += 1
        return term, matrix

    def singularValueDecomposition(self, matrix):
        svd = SingularValueDecomposition(matrix)
        svd.hitung()
        U = svd.getU()
        S = svd.getS()
        Vt = [[j[i] for j in svd.getV()] for i in range(len(svd.getV()))]
        return U, S, Vt

    def countSimilarity(self, term, preprocessingResult, U, S, Vt):

        US = [[0 for i in range(len(S))] for j in range(len(U))]
        SVt = [[0 for i in range(len(Vt))] for j in range(len(S))]
        # USVt = [[0 for i in range(len(Vt))] for j in range(len(US))]
        similarity = [[0 for i in range(len(SVt))] for j in range(len(US[0]))]
        print(len(similarity))
        print(len(similarity[0]))
        print()
        for i in range(len(U)):
            for j in range(len(S)):
                US[i][j] = U[i][j] * S[j]
        for i in range(len(S)):
            for j in range(len(Vt)):
                SVt[i][j] = S[i] * Vt[i][j]

        n = 0
        for doc in preprocessingResult:
            for sentence in doc:
                q = [0 for i in range(len(US[0]))]
                for token in sentence:
                    q = [i + j for i, j in zip(q, US[term.index(token)])]
                q = [i / len(sentence) for i in q]
                qq = sqrt(sum(map(lambda x: x ** 2, q)))
                for i in range(n, len(SVt[0])):
                    d = [row[i] for row in SVt]
                    dd = sqrt(sum(map(lambda x: x ** 2, d)))
                    # print(str(n)+" "+str(i))
                    similarity[n][i] = sum(map(lambda x,y:x*y, q, d)) / (qq * dd)
                n += 1

        for y in similarity:
            print(y)
        # for i in range(len(US)):
        #     for j in range(len(Vt[0])):
        #         for k in range(len(Vt)):
        #             USVt[i][j]+=US[i][k]*Vt[k][j]

        return similarity

    def similarityHistogramClustering(self, similarity, sentencesDocument):
        print('SHC belom')

        # def clusteringkalimat2(self, dokumen):
        #     self.setMatrix(dokumen)
        #     print(self.term)
        #     print(self.matrix)
        #     svd = SingularValueDecomposition(self.matrix)
        #     svd.hitung()
        #     U = svd.getU()
        #     S = svd.getS()
        #     # V = svd.getV()
        #     Vt = [[j[i] for j in svd.getV()] for i in range(len(svd.getV()))]
        #     print(self.matrix)
        #     # for i in range(len(self.matrix)):
        #
        #     # print(S)
        #     # print(Vt)
        #     # self.countSimilarity(dokumen, U, S, Vt)
