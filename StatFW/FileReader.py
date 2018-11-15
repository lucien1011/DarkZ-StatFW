import ROOT,os

fOptionRead = "READ"

class FileReader(object):
    def __init__(self):
        self.fileDict = {}

    def openFile(self,inputDir,sample,TFileName):
        self.fileDict[sample] = ROOT.TFile(os.path.join(inputDir,sample,TFileName),fOptionRead)

    def getObj(self,sample,histName):
        return self.fileDict[sample].Get(histName)

    def end(self):
        for sample,f in self.fileDict.iteritems():
            f.Close()
