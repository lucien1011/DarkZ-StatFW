from collections import OrderedDict

class SystWriter(object):
    def makeMCSystLine(self,binList):
        outputStr = ""
        systDict = OrderedDict()
        for analysisBin in binList:
            for syst in analysisBin.systList:
                if syst.name not in systDict:
                    systDict[syst.name] = syst
        for systName in systDict:
            for analysisBin in binList:    
                systematics = analysisBin.systList
                foundSyst = False
                for systematic in systematics:
                    if systematic.name == systName:
                        foundSyst = True
                        break
                processList = analysisBin.processList
                if systematic.skipDC: continue
                if foundSyst:
                    outputStr += self.makelnNLine(systematic,processList,analysisBin,lineExist=systName in outputStr,forceDash=False)
                else:
                    outputStr += self.makelnNLine(systDict[systName],processList,analysisBin,lineExist=systName in outputStr,forceDash=True)
            outputStr +="\n"
        return outputStr

    @staticmethod
    def makelnNLine(systematic,processList,analysisBin,lineExist=False,forceDash=False,writeNameOnly=False):
        outputStr = ""
        if not lineExist:
            systName = systematic.getSystName() if not systematic.correlation else systematic.correlation(systematic.systNamePrefix,systematic,analysisBin,"",whichType="card")
            outputStr += systName+"\tlnN\t"
        correlationStr = ""
        if not writeNameOnly:
            for eachProcess in processList:
                if eachProcess.name not in systematic.process or forceDash:
                    correlationStr += "-\t"
                elif systematic.magnitude:
                    correlationStr += "%s\t"%systematic.magnitude
                elif systematic.magnitudeFunc:
                    correlationStr += "%s\t"%systematic.magnitudeFunc(systematic,eachProcess.name,analysisBin)
            outputStr += correlationStr
        #outputStr +="\n"
        return outputStr

    @staticmethod
    def makeShapeLine(systematic,processList,analysisBin):
        outputStr = ""
        systName = systematic.getSystName() if not systematic.correlation else systematic.correlation("",systematic,analysisBin,"",whichType="card")
        outputStr += systName+"\tshape\t"
        correlationStr = ""
        for eachProcess in processList:
            if eachProcess.name not in systematic.process:
                correlationStr += "-\t"
            else:
                correlationStr += "1\t"
        outputStr += correlationStr
        outputStr +="\n"
        return outputStr

    @staticmethod
    def makeRateParamLine(rateParamName,binName,process,formulaStr,parameterStr):
        outputStr = ""
        outputStr += rateParamName+"\trateParam\t{binName}\t{process}\t{formulaStr}\t{parameterStr}\n".format(
                process=process,
                binName=binName,
                formulaStr=formulaStr,
                parameterStr=parameterStr,
                )
        return outputStr

    @staticmethod
    def makeParamLine(paramName,meanStr,widthStr,paramRangeStr):
        outputStr = ""
        outputStr += "{paramName}\tparam\t{meanStr}\t{widthStr}\t{paramRangeStr}\n".format(
            paramName=paramName,
            meanStr=meanStr,
            widthStr=widthStr,
            paramRangeStr=paramRangeStr,
            )
        return outputStr+'\n'

    def writeRateParams(self,binList):
        outputStr = ""
        for analysisBin in binList:
            analysisBin.parameterList = []
            for rateParam in analysisBin.rateParams:
                outputStr += self.makeRateParamLine(rateParam.name,analysisBin.name,rateParam.process,rateParam.formulaStr,rateParam.parameterStr)
                for paramStr in rateParam.parameterStr.split(","):
                    if paramStr not in analysisBin.parameterList:
                        analysisBin.parameterList.append(paramStr)
        return outputStr

    def writeParameters(self,binList):
        outputStr = ""
        for analysisBin in binList:
            for paramStr in analysisBin.parameterList:
                if analysisBin.paramDict:
                    outputStr += self.makeParamLine(*analysisBin.paramDict[paramStr])
        return outputStr
