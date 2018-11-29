pdfType_hist = "Hist"
pdfType_BW = "BreitWigner"
pdfType_poly = "Poly"
pdfType_landau = "Landau"
pdfType_data = "Data"
pdfType_dcb = "DCB"

class ShapeFitConfig(object):
    def __init__(self,**kwargs):
        self.__dict__.update(kwargs)
