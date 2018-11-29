import ROOT

ROOT.gSystem.Load("libHiggsAnalysisCombinedLimit.so")

class ShapeFitter(object):
    def __init__(self,obsVarName,obs_low,obs_high):
        self.obsVar = ROOT.RooRealVar(obsVarName,obsVarName,obs_low,obs_high)
        #self.obsVarNorm = ROOT.RooRealVar(obsVarName+"Norm",obsVarName+"Norm",0.,1.)
        #self.obsVar = ROOT.RooFormulaVar(obsVarName,str(obs_high-obs_low)+"*(@0)+"+str(obs_low),ROOT.RooArgList(self.obsVarNorm,))
        #self.obsVarData = ROOT.RooRealVar(obsVarName+"Data",obsVarName+"Data",obs_low,obs_high)

    def makeLandauPdf(self,pdfName,meanVarName,mean_low,mean_high,widthVarName,width_low,width_high):
        meanVar = ROOT.RooRealVar(meanVarName,meanVarName,mean_low,mean_high)
        widthVar = ROOT.RooRealVar(widthVarName,widthVarName,width_low,width_high)
        pdf = ROOT.RooLandau(pdfName,pdfName,self.obsVar,meanVar,widthVar)
        return pdf,meanVar,widthVar
   
    def makeBreitWignerPdf(self,pdfName,meanVarName,mean_low,mean_high,widthVarName,width_low,width_high):
        meanVar = ROOT.RooRealVar(meanVarName,meanVarName,mean_low,mean_high)
        widthVar = ROOT.RooRealVar(widthVarName,widthVarName,width_low,width_high)
        pdf = ROOT.RooBreitWigner(pdfName,pdfName,
                self.obsVar,
                #ROOT.RooRealVar(meanVarName,meanVarName,mean_low,mean_high),
                #ROOT.RooRealVar(widthVarName,widthVarName,width_low,width_high),
                meanVar,
                widthVar,
                )
        return pdf,meanVar,widthVar
        #return pdf
    
    def makeRooHistPdf(self,pdfName,hist):
        dataHist = ROOT.RooDataHist(pdfName+"_RooDataHist","",ROOT.RooArgList(self.obsVar),hist)
        argSet = ROOT.RooArgSet(ROOT.RooArgList(self.obsVar))
        pdf = ROOT.RooHistPdf(
                pdfName,"",
                argSet,
                dataHist,
                )
        return pdf,dataHist,argSet

    def makeBernPdf(self,pdfName,argList):
        pdf = ROOT.RooBernstein(pdfName,pdfName,self.obsVar,ROOT.RooArgList(*argList))
        return pdf

    def makeChebychevPdf(self,pdfName,argList):
        pdf = ROOT.RooChebychev(pdfName,pdfName,self.obsVar,ROOT.RooArgList(*argList))
        return pdf

    def makePolyPdf(self,pdfName,argList,order=0):
        pdf = ROOT.RooPolynomial(pdfName,pdfName,self.obsVar,ROOT.RooArgList(*argList),order)
        return pdf

    def makeGausPdf(self,pdfName,meanVarName,mean_low,mean_high,widthVarName,width_low,width_high):
        meanVar = ROOT.RooRealVar(meanVarName,meanVarName,mean_low,mean_high)
        widthVar = ROOT.RooRealVar(widthVarName,widthVarName,width_low,width_high)
        pdf = ROOT.RooGaussian(pdfName,pdfName,self.obsVar,meanVar,widthVar)
        return pdf,meanVar,widthVar

    def makeBifurGausPdf(self,pdfName,meanVarName,mean_low,mean_high,widthVarName,width_left_low,width_left_high,width_right_low,width_right_high):
        meanVar = ROOT.RooRealVar(meanVarName,meanVarName,mean_low,mean_high)
        widthLeftVar = ROOT.RooRealVar(widthVarName+"L",widthVarName,width_left_low,width_left_high)
        widthRightVar = ROOT.RooRealVar(widthVarName+"R",widthVarName,width_right_low,width_right_high)
        pdf = ROOT.RooBifurGauss(pdfName,pdfName,self.obsVar,meanVar,widthLeftVar,widthRightVar)
        return pdf,meanVar,widthLeftVar,widthRightVar

    def makeDoubleCBPdf(self,pdfName,
            meanVarName,mean_low,mean_high,
            widthVarName,width_low,width_high,
            alphaLVarName,alphaL_low,alphaL_high,
            alphaRVarName,alphaR_low,alphaR_high,
            nLVarName,nL_low,nL_high,
            nRVarName,nR_low,nR_high,
            ):
        meanVar = ROOT.RooRealVar(meanVarName,meanVarName,mean_low,mean_high)
        widthVar = ROOT.RooRealVar(widthVarName,widthVarName,width_low,width_high)
        alphaLVar = ROOT.RooRealVar(alphaLVarName,alphaLVarName,alphaL_low,alphaL_high)
        alphaRVar = ROOT.RooRealVar(alphaRVarName,alphaRVarName,alphaR_low,alphaR_high)
        nLVar = ROOT.RooRealVar(nLVarName,nLVarName,nL_low,nL_high)
        nRVar = ROOT.RooRealVar(nRVarName,nRVarName,nR_low,nR_high)
        pdf = ROOT.RooDoubleCB(pdfName,pdfName,self.obsVar,meanVar,widthVar,alphaLVar,alphaRVar,nLVar,nRVar)
        return pdf,meanVar,widthVar,alphaLVar,alphaRVar,nLVar,nRVar

    def makeCBPdf(self,pdfName,
            meanVarName,mean_low,mean_high,
            widthVarName,width_low,width_high,
            alphaVarName,alpha_low,alpha_high,
            nVarName,n_low,n_high,):
        meanVar = ROOT.RooRealVar(meanVarName,meanVarName,mean_low,mean_high)
        widthVar = ROOT.RooRealVar(widthVarName,widthVarName,width_low,width_high)
        alphaVar = ROOT.RooRealVar(alphaVarName,alphaVarName,alpha_low,alpha_high)
        nVar = ROOT.RooRealVar(nVarName,nVarName,n_low,n_high)
        pdf = ROOT.RooCBShape(pdfName,pdfName,self.obsVar,meanVar,widthVar,alphaVar,nVar)
        return pdf,meanVar,widthVar,alphaVar,nVar

    def makeExpPdf(self,pdfName,widthVarName,width_low,width_high,):
        widthVar = ROOT.RooRealVar(widthVarName,widthVarName,width_low,width_high)
        pdf = ROOT.RooExponential(pdfName,pdfName,self.obsVar,widthVar)
        return pdf,widthVar

    def makeChiSquarePdf(self,pdfName,nVarName,n_low,n_high):
        nVar = ROOT.RooRealVar(nVarName,nVarName,n_low,n_high)
        pdf = ROOT.RooChiSquarePdf(pdfName,pdfName,self.obsVar,nVar)
        return pdf,nVar

    def addPdf(self,pdfName,pdf1,pdf2):
        coeffVar = ROOT.RooRealVar(pdfName+"_coeff","",0.5,0.,1.)
        pdf = ROOT.RooAddPdf(pdfName,pdfName,pdf1,pdf2,coeffVar)
        return pdf,coeffVar

    def prodPdf(self,pdfName,pdf1,pdf2):
        pdf = ROOT.RooProdPdf(pdfName,pdfName,pdf1,pdf2)
        return pdf

    def end(self):
        del self.obsVarNorm
        del self.obsVar
        del self.obsVarData
