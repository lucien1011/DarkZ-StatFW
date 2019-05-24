class BrInfo(object):
    def __init__(self,mass,Gamma_Zd,Br_ZdTo2l,Br_HToZZdTo4l,Br_HToZdZdTo4l):
        self.mass = mass
        self.Gamma_Zd = Gamma_Zd
        self.Br_ZdTo2l = Br_ZdTo2l
        self.Br_HToZZdTo4l = Br_HToZZdTo4l
        self.Br_HToZdZdTo4l = Br_HToZdZdTo4l

class BrTableReader(object):
    def __init__(self):
        self.infoDict = {}

    def addInfo(self,mass,Gamma_Zd,Br_ZdTo2l,Br_HToZZdTo4l,Br_HToZdZdTo4l,forceAdd=False):
        if mass not in self.infoDict or forceAdd:
            self.infoDict[mass] = BrInfo(mass,Gamma_Zd,Br_ZdTo2l,Br_HToZZdTo4l,Br_HToZdZdTo4l)
