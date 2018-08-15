class Bin(object):
    """
    A class to input informtion for each bin in the data card, i.e. 4mu, 4e and 2e2mu
    """
    def __init__(self,name,signalName="HZZd",sysFile="test.txt"):
        self.name = name
        self.processList = []
        self.signalName = signalName
        self.sysFile = systFile
       
    def isSignal(self,name):
        return "HZZd" in self.signalName 
