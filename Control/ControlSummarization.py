from math import sqrt
from math import log10
from Control.SingularValueDecomposition1 import SingularValueDecomposition1
from Control.SingularValueDecomposition import SingularValueDecomposition
from Entity.EntitySummarization import EntitySummarization


class ControlSummarization:
    entitySummaries = EntitySummarization()
    svd = SingularValueDecomposition()

    def doSummarization(self, preprocessingResult, sentencesDocument):

        # similarity, listCluster = self.sentencesClustering(preprocessingResult)
        similarity = self.latentSemancticIndexing(preprocessingResult)
        listCluster = self.similarityHistogramClustering(similarity)
        listSentence = self.representativeSelection(similarity, sentencesDocument, listCluster)
        self.entitySummaries.setSummary(listSentence)

    def getResultSummary(self):
        return self.entitySummaries.getSummary()

    # def sentencesClustering(self, preprocessingResult):
    #     similarity = self.latentSemancticIndexing(preprocessingResult)
    #     listCluster = self.similarityHistogramClustering(similarity)
    #     return similarity, listCluster

    def latentSemancticIndexing(self, preprocessingResult):
        # term, matrix = self.setMatrix(preprocessingResult)
        matrix = []  # term x sentence
        term = []  # term x 1
        iColumn = 0
        nColumn = len(preprocessingResult)
        for sentence in preprocessingResult:
            for token in sentence:
                if token in term:
                    matrix[term.index(token)][iColumn] += 1
                else:
                    term.append(token)
                    matrix.append([0] * nColumn)
                    matrix[len(term) - 1][iColumn] = 1
            iColumn += 1

        # U, S, Vt = self.singularValueDecomposition(matrix)

        self.svd.count(matrix)
        U = self.svd.getU()
        S = self.svd.getS()
        Vt = self.svd.getVt()

        similarity = self.countSimilarity(term, preprocessingResult, U, S, Vt)
        return similarity

    def countSimilarity(self, term, preprocessingResult, U, S, Vt):
        US = [x[:] for x in [[0] * len(S)] * len(U)]
        SVt = [x[:] for x in [[0] * len(Vt)] * len(S)]
        similarity = [x[:] for x in [[0] * len(SVt)] * len(SVt[0])]
        for i in range(len(U)):
            for j in range(len(S)):
                US[i][j] = U[i][j] * S[j]
        for i in range(len(S)):
            for j in range(len(Vt)):
                SVt[i][j] = S[i] * Vt[i][j]

        n = 0
        for sentence in preprocessingResult:
            q = [0] * len(US[0])
            for token in sentence:
                q = [i + j for i, j in zip(q, US[term.index(token)])]
            q = [i / len(sentence) for i in q]

            qq = sqrt(sum(list(map(lambda x: x ** 2, q))))

            for i in range(n, len(SVt[0])):
                d = [row[i] for row in SVt]
                dd = sqrt(sum(list(map(lambda x: x ** 2, d))))
                if n != i:
                    similarity[n][i] = similarity[i][n] = sum(list(map(lambda x, y: x * y, q, d))) / (qq * dd)
            n += 1
        return similarity

    def similarityHistogramClustering(self, similarity):
        HRmin = 0.6
        epsilon = 0.4
        similarityThreshold = 0.7 - 0.05
        listCluster = []
        c = [0]
        listCluster.append(c)
        HRold = [0]
        HRnew = [0]

        def countHistogramRatio(cluster):
            count = 0
            n = len(cluster)
            if n > 1:
                for i in range(0, n - 1):
                    x = cluster[i]
                    for j in range(i + 1, n):
                        y = cluster[j]
                        if similarity[x][y] > (similarityThreshold):
                            count += 1
                return count / (n * (n - 1) / 2)
            else:
                return 0

        for i in range(1, len(similarity)):
            foundCluster = False
            for j in range(len(listCluster)):
                if foundCluster is False:
                    if HRold[j] == 0:
                        HRold[j] = countHistogramRatio(listCluster[j])
                    listCluster[j].append(i)
                    HRnew[j] = countHistogramRatio(listCluster[j])
                    if (HRnew[j] >= HRold[j]) or ((HRnew[j] > HRmin) and (HRold[j] - HRnew[j]) < epsilon):
                        foundCluster = True
                        HRnew[j] = HRold[j]
                    else:
                        listCluster[j].pop()
            if foundCluster is False:
                c = [i]
                listCluster.append(c)
                HRold.append(0)
                HRnew.append(0)
        # print(len(listCluster))
        # for list in listCluster:
        #     print(list)
        # print()
        return listCluster

    def representativeSelection(self, similarity, sentencesDocument, listCluster):
        threshold =0.7
        listSentence = []
        maxW = []
        for i in range(len(listCluster)):
            max = []
            for j in listCluster[i]:
                max.append(0)
                for k in listCluster[i]:
                    if similarity[j][k] > max[-1]:
                        max[-1] = similarity[j][k]
            maxW.append(sum(max))

        for i in range(len(listCluster)):
            x = -1
            Fsid = 0
            for j in listCluster[i]:
                W = 0
                for k in listCluster[i]:
                    if similarity[j][k] > threshold:
                        W += similarity[j][k]

                if (maxW[i] > 0):
                    if (W / maxW[i]) > Fsid:
                        x = j
                        Fsid = W / maxW[i]

                if (x == -1): x = listCluster[i][0]
            listSentence.append(sentencesDocument[x] + ".")

        return listSentence


        # def setMatrix(self, preprocessingResult):
        #     matrix = []  # term x sentence
        #     term = []  # term x 1
        #     iColumn = 0
        #     nColumn = len(preprocessingResult)
        #     for sentence in preprocessingResult:
        #         for token in sentence:
        #             if token in term:
        #                 matrix[term.index(token)][iColumn] += 1
        #             else:
        #                 term.append(token)
        #                 matrix.append([0] * nColumn)
        #                 matrix[len(term) - 1][iColumn] = 1
        #         iColumn += 1
        #     return term, matrix
        #
        # def singularValueDecomposition(self, matrix):
        #     svd = SingularValueDecomposition(matrix)
        #     svd.count()
        #     U = svd.getU()
        #     S = svd.getS()
        #     Vt = svd.getVt()
        #     return U,S,Vt
        # svd = SingularValueDecomposition1(matrix)
        # svd.count()
        # U = svd.getU()
        # S = svd.getS()
        # Vt = [[j[i] for j in svd.getV()] for i in range(len(svd.getV()))]
        # return  U, S, Vt
        # def clusterOrdering(self, listCluster, document):
        #     threshold = 10
        #     weight = []
        #     for cluster in listCluster:
        #         w = 0
        #         t = {}
        #         for i in cluster:
        #             for term in document[i]:
        #                 if term in t.keys():
        #                     t[term] += 1
        #                 else:
        #                     t[term] = 1
        #         for value in t.values():
        #             if value > threshold:
        #                 w += log10(value)
        #         weight.append(w)
        #     return weight
