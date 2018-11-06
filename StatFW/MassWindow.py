class MassWindow(object):
    def __init__(self,name,central_value,width):
        self.central_value = central_value
        self.width = width
        self.lower = central_value*(1-self.width)
        self.higher = central_value*(1+self.width)
        self.processList = []
        self.name = name

    def makeHistName(self):
        #return "_".join([str(self.central_value),str(self.width)])
        return self.name

    def inWindow(self,value):
        return value > self.lower and value < self.higher

    def getBinName(self):
        return "window_"+str(self.central_value)+"_"+str(self.width).replace(".","p")

    def matchSample(self,sampleName):
        return str(self.central_value) in sampleName
