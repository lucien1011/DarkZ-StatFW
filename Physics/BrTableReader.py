import bisect

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

    def interpolate(self,mass,attrName):
        if mass in self.infoDict:
            return getattr(self.infoDict[mass],attrName)
        else:
            massList = self.infoDict.keys()
            massList.sort()
            index = bisect.bisect(massList,mass)
            low_m = massList[index-1]
            high_m = massList[index]
            low_value = getattr(self.infoDict[low_m],attrName)
            high_value = getattr(self.infoDict[high_m],attrName)
            return low_value+(high_value-low_value)/(high_m-low_m)*(mass-low_m)

