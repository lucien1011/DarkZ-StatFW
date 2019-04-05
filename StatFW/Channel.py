class Bin(object):
    """
    A class to input informtion for each bin in the data card, i.e. 4mu, 4e and 2e2mu
    """
    def __init__(self,name,signalNames=["HZZd"],sysFile="test.txt",inputBinName="",width=None,parameterDict=None,parameterList=[]):
        self.name = name
        self.processList = []
        self.signalNames = signalNames
        self.sysFile = sysFile
        self.inputBinName = inputBinName
        self.width = width
        self.rateParams = []
        self.paramDict = {}
        self.parameterDict = parameterDict
        self.parameterList = parameterList
       
    def isSignal(self,name):
        return any([name.startswith(s) for s in self.signalNames])
