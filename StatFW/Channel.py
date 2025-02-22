class Bin(object):
    """
    A class to input informtion for each bin in the data card, i.e. 4mu, 4e and 2e2mu
    """
    def __init__(self,name,signalNames=["HZZd"],sysFile="test.txt",inputBinName="",width=None,parameterDict=None,parameterList=[],central_value=None,x_width=None,y_width=None):
        self.name = name
        self.processList = []
        self.signalNames = signalNames
        self.sysFile = sysFile
        self.inputBinName = inputBinName
        self.width = width
        self.x_width = x_width
        self.y_width = y_width
        self.rateParams = []
        self.paramDict = {}
        self.parameterDict = parameterDict
        self.parameterList = parameterList
        self.central_value = central_value
       
    def isSignal(self,name):
        return any([name.startswith(s) for s in self.signalNames])
