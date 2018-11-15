class Bin(object):
    """
    A class to input informtion for each bin in the data card, i.e. 4mu, 4e and 2e2mu
    """
    def __init__(self,name,signalName="HZZd",sysFile="test.txt",inputBinName="",width=None):
        self.name = name
        self.processList = []
        self.signalName = signalName
        self.sysFile = sysFile
        self.inputBinName = inputBinName
        self.width = width
        self.rateParams = []
        self.paramDict = {}
       
    def isSignal(self,name):
        return self.signalName in name
