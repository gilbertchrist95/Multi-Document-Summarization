from threading import Thread
from math import sqrt
from math import log10
from Control.SingularValueDecomposition import SingularValueDecomposition


class ControlSummarization:

    def doSummarization(self, preprocessingResult, sentencesDocument):
        document = [item for sublist in preprocessingResult for item in sublist]
        similarity, listCluster = self.sentencesClustering(preprocessingResult, sentencesDocument)
        weight = self.clusterOrdering(listCluster, document)
        # weight = self.clusterOrdering(listCluster, document)
        listSentence = self.representativeSelection(similarity, sentencesDocument, listCluster)
        # listSentence = self.representativeSelection(similarity, sentencesDocument, listCluster)
        return listSentence

    def sentencesClustering(self, preprocessingResult, sentencesDocument):
        similarity = self.latentSemancticIndexing(preprocessingResult)
        if len(similarity) != len(sentencesDocument):
            print('something wrong  !')
            exit()
        listCluster = self.similarityHistogramClustering(similarity)
        return similarity, listCluster

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

        # US = [[0 for i in range(len(S))] for j in range(len(U))]
        US = [x[:] for x in [[0] * len(S)] * len(U)]
        # SVt = [[0 for i in range(len(Vt))] for j in range(len(S))]
        SVt = [x[:] for x in [[0] * len(Vt)] * len(S)]
        # USVt = [[0 for i in range(len(Vt))] for j in range(len(US))]
        # similarity = [[0 for i in range(len(SVt))] for j in range(len(US[0]))]
        similarity = [x[:] for x in [[0] * len(SVt)] * len(US[0])]
        # print(len(similarity))
        # print(len(similarity[0]))
        for i in range(len(U)):
            for j in range(len(S)):
                US[i][j] = U[i][j] * S[j]
        for i in range(len(S)):
            for j in range(len(Vt)):
                SVt[i][j] = S[i] * Vt[i][j]

        n = 0
        for doc in preprocessingResult:
            for sentence in doc:
                q = [0] * len(US[0])
                for token in sentence:
                    q = [i + j for i, j in zip(q, US[term.index(token)])]
                # print(sentence)
                q = [i / len(sentence) for i in q]
                qq = sqrt(sum(map(lambda x: x ** 2, q)))
                for i in range(n, len(SVt[0])):
                    d = [row[i] for row in SVt]
                    dd = sqrt(sum(map(lambda x: x ** 2, d)))
                    # print(str(n)+" "+str(i))
                    if n != i:
                        similarity[n][i] = similarity[i][n] = sum(map(lambda x, y: x * y, q, d)) / (qq * dd)
                n += 1
        return similarity

    def latentSemancticIndexing(self, preprocessingResult):
        term, matrix = self.setMatrix(preprocessingResult)
        U, S, Vt = self.singularValueDecomposition(matrix)
        similarity = self.countSimilarity(term, preprocessingResult, U, S, Vt)
        return similarity

    def similarityHistogramClustering(self, similarity):
        HRmin = 0.7
        epsilon = 0.2
        listCluster = []
        c = [0]
        listCluster.append(c)
        HRold = [0]
        HRnew = [0]

        def countHistogramRatio(cluster, similarity):
            similarityThreshold = 0.6
            count = 0
            n = len(cluster)
            if n > 1:
                for i in range(0, n - 1):
                    x = cluster[i]
                    for j in range(i + 1, n):
                        y = cluster[j]
                        if (similarity[x][y] > similarityThreshold - 0.05):
                            count += 1
                return count / (n * (n - 1) / 2)
            else:
                return 0

        for i in range(1, len(similarity)):
            foundCluster = False
            for j in range(len(listCluster)):
                if HRold[j] == 0:
                    HRold[j] = countHistogramRatio(listCluster[j], similarity)
                listCluster[j].append(i)
                HRnew[j] = countHistogramRatio(listCluster[j], similarity)
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

        return listCluster

    def clusterOrdering(self, listCluster, document):
        threshold = 10
        weight = []
        for cluster in listCluster:
            w = 0
            t = {}
            for i in cluster:
                for term in document[i]:
                    if term in t.keys():
                        t[term] += 1
                    else:
                        t[term] = 1
            for value in t.values():
                if value > threshold:
                    w += log10(value)
            weight.append(w)
        return weight

    def representativeSelection(self, similarity, sentencesDocument, listCluster):
        threshold = 0.5
        listSentence = []

        maxW=[0]*len(listCluster)

        for i in range(len(listCluster)):
            for j in listCluster[i]:
                maxW[i]+=(max(similarity[j]))

        for i in range(len(listCluster)):
            W = 0
            x = -1
            Fsid=0
            for j in listCluster[i]:
                for k in listCluster[i]:
                    if similarity[j][k]>threshold:
                        W+=similarity[j][k]
                if (W/maxW[i])>Fsid:
                    x = j
                    Fsid = W/maxW[i]
            listSentence.append(sentencesDocument[x]+".")

        return listSentence