from StatFW.SystWriter import *
import os

class CardConfig(object):
    def __init__(self,name):
        self.name = name
        self.shapeStr = None

class DataCard(object):
    def __init__(self,config):
        self.sep = "---------------------------------------------------------------------------------"
        self.tagStr = "\t"
        self.config = config

    def getBinName(self):
        return self.config.name

    #def makeHeader(self,rootFilePath):
    def makeHeader(self):
        header = '''
*     number of categories
*     number of samples minus one
*     number of nuisance parameters
-----------------------------------------------------------------------
'''
        #header += "shapes * {} $CHANNEL/$PROCESS $CHANNEL/$PROCESS_$SYSTEMATIC\n".format(rootFilePath.split("/")[-1])
        if not self.config.shapeStr:
            header += "shapes * * FAKE\n"
        else:
            header += self.config.shapeStr
        header += self.sep+"\n"
        header += "\n"
        return header

    def makeStandardCardDetails(self,binList):
        self.rateParamLines = ""
        tagStr = self.tagStr
        self.binName = "bin"+tagStr
        self.processName = "process"+tagStr
        self.processNum = "process"+tagStr
        self.binNameObservation = "bin"+tagStr
        for bin in binList:
            self.binNameObservation += bin.name+tagStr
            for iprocess,process in enumerate(bin.processList):
                self.binName += bin.name+tagStr
                self.processName += process.name+tagStr
                if bin.isSignal(process.name):
                    self.processNum += str(-iprocess)+tagStr
                else:
                    self.processNum += str(iprocess+1)+tagStr
        self.observation = "observation"
        self.rates = "rate"+self.tagStr
        self.sep = "---------------------------------------------------------------------------------"
        self.systLines = ""
        return  

    def makeObservationLine(self,binList):
        line = ""
        line += self.observation+"\t"
        for bin in binList:
            line += str(bin.data.count)+"\t"
        line += "\n"
        return line

    def makeCard(self,outputDir,binList,appendToPath=""):
        outputStr = ""

        self.makeStandardCardDetails(binList)
        
        binName = self.getBinName()
        
        outputStr = self.makeHeader()
        outputStr += self.binNameObservation+"\n"
        outputStr += self.makeObservationLine(binList)
        outputStr += self.sep+"\n"
        outputStr += self.binName+"\n"
        outputStr += "\n"
        outputStr += "\n"

        outputStr += self.processName+"\n"
        outputStr += self.processNum+"\n"

        outputStr += self.rates+"\t"
        for bin in binList:
            for process in bin.processList:
                #outputStr += "%10.8f"%process.count+self.tagStr*2
                outputStr += str(process.count)+self.tagStr*2
        outputStr += "\n"
        outputStr += self.sep+"\n"
        outputStr += "\n"

        systWriter = SystWriter()
        outputStr += systWriter.makeMCSystLine(binList)
        outputStr += "\n"
        outputStr += systWriter.writeRateParams(binList)
        outputStr += systWriter.writeParameters(binList)

        outputPath = os.path.join(outputDir,self.makeOutFileName(".txt",appendToPath))

        outputFile = open(outputPath,"w")
        outputFile.write(outputStr)
        outputFile.close()

    def makeOutFileName(self,extension,appendToPath):
        outputPath = self.getBinName()+extension if not appendToPath else self.getBinName()+"_"+appendToPath+extension
        return outputPath
