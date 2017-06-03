from Entity.EntityAccuration import EntityAccuration
from Control.FilteringController import FilteringController
from Control.StemmingController import StemmingController
import re


class AccurationController:
    def __init__(self):
        self.controlFiltering = FilteringController()
        self.controlStemming = StemmingController()
        self.ngram = 1;
        self.entityAccuration = EntityAccuration()
        DELIMETERS = "\"", "\'", "{", "}", "(", ")", "[", "]", ">", "<", "_", "=", "+", "|", "\\", ":", ";", " ", ",", ".", "/", "?", "~", "!", "@", "#", "$", "%", "^", "&", "*", "\r", "\n", "\t", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"
        self.regexPattern = '|'.join(map(re.escape, DELIMETERS))

    def doAccuration(self, summaries, resultSummary):
        resultSummary = self.setGramResultSummary(resultSummary)
        summaries = self.setGramManualSummaries(summaries)
        accuration = self.countAccuration(resultSummary, summaries)
        self.entityAccuration.setAccuration(accuration)

    def getResultAccuration(self):
        return self.entityAccuration.getAccuration()

    def setGramResultSummary(self, summary):
        summary = list(filter(None, re.split(self.regexPattern, ' '.join(summary).lower())))
        print(summary)
        # summary = list(re.split(self.regexPattern, ' '.join(summary).lower()))
        summary = self.controlFiltering.doFiltering(summary)
        summary = self.controlStemming.doStemming(summary)
        grams = [summary[i:i + self.ngram] for i in range(len(summary) - self.ngram + 1)]
        print(grams)
        return grams

    def setGramManualSummaries(self, summaries):
        gramss = {}
        for summary in summaries:
            summaries[summary] = list(filter(None, re.split(self.regexPattern, summaries[summary].lower())))
                # summaries[summary] = list( re.split(self.regexPattern, summaries[summary].lower()))
            summaries[summary] = self.controlFiltering.doFiltering(summaries[summary])
            summaries[summary] = self.controlStemming.doStemming(summaries[summary])
            gramss[summary] = [summaries[summary][i:i + self.ngram] for i in
                               range(len(summaries[summary]) - self.ngram + 1)]
        return gramss

    def countAccuration(self, resultSummary, summaries):
        accurations = {}
        for summary in summaries:
            accuration = []
            count = 0
            for token in resultSummary:
                if token in summaries[summary]:
                    count += 1
            recall = count / len(summaries[summary])
            accuration.append(recall)
            precision = count / len(resultSummary)
            accuration.append(precision)
            fmeasure = (2 * recall * precision) / (recall + precision)
            accuration.append(fmeasure)
            accurations[summary] = accuration
        return accurations

    # def setGram2(self, summaries, resultSummary):
    #     # for summary in summaries:
    #     #     summaries[summary] = list(set(filter(None, re.split(regexPattern, summaries[summary].lower()))))
    #     # resultSummary = list(set(filter(None, re.split(regexPattern, ' '.join(resultSummary).lower()))))
    #     for summary in summaries:
    #         summaries[summary] = list(filter(None, re.split(self.regexPattern, summaries[summary].lower())))
    #     resultSummary = list(filter(None, re.split(self.regexPattern, ' '.join(resultSummary).lower())))
    #     return resultSummary, summaries
        # def countRouge(self, resultSummary, summaries):
        #     accurations = {}
        #     count1 = 0
        #     count2 = 0
        #     count3 = 0
        #     accuration = []
        #     for summary in summaries:
        #
        #         count = 0
        #         for token in resultSummary:
        #             if token in summaries[summary]:
        #                 count += 1
        #         # accuration.append(count)
        #         # accuration.append(len(summaries[summary]))
        #         count1 += count
        #         count2 += len(summaries[summary])
        #         count3 += len(resultSummary)
        #
        #     recall = count1/count2
        #     precision = count1/count3
        #     fmeasure = (2*recall*precision)/(recall+precision)
        #     accuration.append(recall)
        #     accuration.append(precision)
        #     accuration.append(fmeasure)
        #     accurations['hasil'] = accuration
        #
        #
        #         # recall = count / len(summaries[summary])
        #         # accuration.append(recall)
        #         # precision = count / len(resultSummary)
        #         # accuration.append(precision)
        #         # fmeasure = (2*recall*precision)/(recall+precision)
        #         # accuration.append(fmeasure)
        #         # accurations[summary] = accuration
        #
        #     # for summary in summaries:
        #     #     count=0
        #     #     for token in summaries[summary]:
        #     #         if token in resultSummary:
        #     #             count+=1
        #     #     accuration[summary] = count / len(summaries[summary])
        #     # print(accuration)
        #     return accurations
        # for summary in summaries:
        #     count=0
        #     for token in summaries[summary]:
        #         if token in resultSummary:
        #             count+=1
        #     accuration[summary] = count / len(summaries[summary])
        # print(accuration)
