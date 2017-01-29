from Entity.EntityAccuration import EntityAccuration
import re

class ControlAccuration:
    entityAccuration= EntityAccuration()

    def doAccuration(self, summaries, resultSummary):
        resultSummary, summaries = self.setGram(summaries, resultSummary)
        accuration = self.countRouge1(resultSummary,summaries)
        self.entityAccuration.setAccuration(accuration)

    def getResultAccuration(self):
        return self.entityAccuration.getAccuration()

    def setGram(self, summaries, resultSummary):
        DELIMETERS = "\"", "\'", "{", "}", "(", ")", "[", "]", ">", "<", "_", "=", "+", "|", "\\", ":", ";", " ", ",", ".", "/", "?", "~", "!", "@", "#", "$", "%", "^", "&", "*", "\r", "\n", "\t", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"
        regexPattern = '|'.join(map(re.escape, DELIMETERS))
        for summary in summaries:
            summaries[summary] = list(set(filter(None, re.split(regexPattern, summaries[summary].lower()))))
        resultSummary = list(set(filter(None, re.split(regexPattern, ' '.join(resultSummary).lower()))))
        return resultSummary, summaries

    def countRouge1(self, resultSummary, summaries):
        accuration = {}
        for summary in summaries:
            count = 0
            for token in resultSummary:
                if token in summaries[summary]:
                    count += 1
            accuration[summary] = count / len(summaries[summary])
        return accuration
