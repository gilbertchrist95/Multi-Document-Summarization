from Entity.EntityAccuration import EntityAccuration
import re


class ControlAccuration:


    def __init__(self):
        self.entityAccuration = EntityAccuration()
        DELIMETERS = "\"", "\'", "{", "}", "(", ")", "[", "]", ">", "<", "_", "=", "+", "|", "\\", ":", ";", " ", ",", ".", "/", "?", "~", "!", "@", "#", "$", "%", "^", "&", "*", "\r", "\n", "\t", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"
        self.regexPattern = '|'.join(map(re.escape, DELIMETERS))

    def doAccuration(self, summaries, resultSummary):
        resultSummary = self.setGramResultSummary(resultSummary)
        summaries = self.setGramManualSummaries(summaries)

        accuration = self.countRouge1(resultSummary,summaries)
        self.entityAccuration.setAccuration(accuration)

    def getResultAccuration(self):
        return self.entityAccuration.getAccuration()

    # def setGram2(self, summaries, resultSummary):
    #     # for summary in summaries:
    #     #     summaries[summary] = list(set(filter(None, re.split(regexPattern, summaries[summary].lower()))))
    #     # resultSummary = list(set(filter(None, re.split(regexPattern, ' '.join(resultSummary).lower()))))
    #     for summary in summaries:
    #         summaries[summary] = list(filter(None, re.split(self.regexPattern, summaries[summary].lower())))
    #     resultSummary = list(filter(None, re.split(self.regexPattern, ' '.join(resultSummary).lower())))
    #     return resultSummary, summaries

    def setGramResultSummary(self,summary):
        summary = list(filter(None, re.split(self.regexPattern, ' '.join(summary).lower())))
        return summary

    def setGramManualSummaries(self,summaries):
        for summary in summaries:
            summaries[summary] = list(filter(None, re.split(self.regexPattern, summaries[summary].lower())))
        return summaries

    def countRouge1(self, resultSummary, summaries):
        accurations = {}


        for summary in summaries:
            accuration = []
            count = 0
            for token in resultSummary:
                if token in summaries[summary]:
                    count += 1
            accuration.append(count)
            accuration.append(len(summaries[summary]))
            accuration.append(count / len(summaries[summary]))
            accurations[summary] = accuration
        # for summary in summaries:
        #     count=0
        #     for token in summaries[summary]:
        #         if token in resultSummary:
        #             count+=1
        #     accuration[summary] = count / len(summaries[summary])
        # print(accuration)
        return accurations

