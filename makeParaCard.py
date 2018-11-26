import os,copy,math,argparse,ROOT

from StatFW.DataCard import DataCard,CardConfig
from StatFW.Systematic import *
from StatFW.Process import *
from StatFW.Reader import *
from StatFW.Channel import Bin
from StatFW.FileReader import FileReader
from StatFW.RateParameter import RateParameter

from Dataset.MergeSampleDict import mergeSampleDict

from Parametric.InputParameters import parameterDict
from Parametric.ShapeFitConfig import pdfType_hist,pdfType_BW,pdfType_poly,pdfType_landau,pdfType_data
from Parametric.ShapeFitter import ShapeFitter

shapeStr = "shapes * TwoEl_SR shape_TwoEl_SR.root parametric_pdf_TwoEl_SR:$PROCESS\n"
shapeStr += "shapes * TwoMu_SR shape_TwoMu_SR.root parametric_pdf_TwoMu_SR:$PROCESS\n"

def getCountAndError(hist,central,width,isSR=True):
    lower_value = central-width
    upper_value = central+width

    if isSR:
        error = ROOT.Double(0.)
        integral = hist.IntegralAndError(
                hist.GetXaxis().FindFixBin(lower_value),
                hist.GetXaxis().FindFixBin(upper_value),
                error,
                )
    else:
        error1 = ROOT.Double(0.)
        integral1 = hist.IntegralAndError(
                0,
                hist.GetXaxis().FindFixBin(lower_value)-1,
                error1,
                )
        error2 = ROOT.Double(0.)
        integral2 = hist.IntegralAndError(
                hist.GetXaxis().FindFixBin(upper_value)+1,
                hist.GetNbinsX()+1,
                error2,
                )
        integral = integral1+integral2
        error = math.sqrt(error1**2+error2**2)
    return integral,error

def getIntegral(hist):
    error = ROOT.Double(0.)
    integral = hist.IntegralAndError(
            #0,
            #hist.GetNbinsX()+1,
            1,
            hist.GetNbinsX(),
            error,
            )
    return integral,error
# ____________________________________________________________________________________________________________________________________________ ||
parser = argparse.ArgumentParser()
parser.add_argument("--inputDir",action="store")
parser.add_argument("--outputDir",action="store")
parser.add_argument("--verbose",action="store_true")
parser.add_argument("--parametric",action="store_true")
parser.add_argument("--drawDir",action="store")

option = parser.parse_args()

# ____________________________________________________________________________________________________________________________________________ ||
# Configurable
inputDir = option.inputDir
commonLnSystFilePath = "/home/lucien/Higgs/DarkZ/DarkZ-StatFW/Config/CommonSyst_2mu2e.txt"
lnSystFilePathDict = {
        #"FourEl": "/home/lucien/Higgs/DarkZ/DarkZ-StatFW/Config/Syst_4e.txt", 
        #"FourMu": "/home/lucien/Higgs/DarkZ/DarkZ-StatFW/Config/Syst_4mu.txt", 
        #"TwoElTwoMu": "/home/lucien/Higgs/DarkZ/DarkZ-StatFW/Config/Syst_2e2mu.txt", 
        #"TwoMuTwoEl": "/home/lucien/Higgs/DarkZ/DarkZ-StatFW/Config/Syst_2mu2e.txt", 
        "TwoMu": "/home/lucien/Higgs/DarkZ/DarkZ-StatFW/Config/Syst_2mu.txt", 
        "TwoEl": "/home/lucien/Higgs/DarkZ/DarkZ-StatFW/Config/Syst_2e.txt", 
        }
outputDir = option.outputDir
TFileName = "StatInput.root"

# ____________________________________________________________________________________________________________________________________________ ||
# mass window
signal_model_names = [
        #"HZZd_M10",  
        #"HZZd_M15",  
        #"HZZd_M20",  
        #"HZZd_M25",  
        #"HZZd_M30",  
        #"HZZd_M4", 
        "HZZd_M7",
        ]

data_names = [
        "Data2016",
        ]

#bkg_names = mergeSampleDict.keys()
bkg_names = [
        "Higgs",
        "qqZZ",
        "ggZZ",
        "ZPlusX",
        ]

# ____________________________________________________________________________________________________________________________________________ ||
# bin list
binList = [
        #Bin("FourEl",sysFile=lnSystFilePathDict["FourEl"],inputBinName="4e",),
        #Bin("FourMu",sysFile=lnSystFilePathDict["FourMu"],inputBinName="4mu",),
        #Bin("TwoElTwoMu",sysFile=lnSystFilePathDict["TwoElTwoMu"],inputBinName="2e2mu"),
        #Bin("TwoMuTwoEl",sysFile=lnSystFilePathDict["TwoMuTwoEl"],inputBinName="2mu2e"),
        Bin("TwoEl_SR",sysFile=lnSystFilePathDict["TwoEl"],inputBinName="2e-Norm",width=0.05),
        Bin("TwoMu_SR",sysFile=lnSystFilePathDict["TwoMu"],inputBinName="2mu-Norm",width=0.02),
        ]

# ____________________________________________________________________________________________________________________________________________ ||
# syst
lnSystReader = LogNormalSystReader()
commonLnSystematics = lnSystReader.makeLnSyst(commonLnSystFilePath)

# ____________________________________________________________________________________________________________________________________________ ||
reader = FileReader()

if not os.path.exists(os.path.abspath(outputDir)):
    os.makedirs(os.path.abspath(outputDir))

if option.parametric:
    fitter = ShapeFitter("massZ2",0.,1.)

for signal_model_name in signal_model_names:
    reader.openFile(inputDir,signal_model_name,TFileName)
    if option.verbose: print "*"*100
    if option.verbose: print "Making data card for ",signal_model_name
    
    config = CardConfig(signal_model_name)
    config.shapeStr = shapeStr
    dataCard = DataCard(config) 
    cardDir = outputDir+"/"+dataCard.makeOutFileName("/","")
    if not os.path.exists(os.path.abspath(cardDir)):
        os.makedirs(os.path.abspath(cardDir))

    central_value = float(signal_model_name.replace("HZZd_M",""))
    binListCopy = copy.deepcopy(binList)
    for ibin,bin in enumerate(binListCopy):
        if option.verbose: print "-"*20
        if option.verbose: print bin.name
        histName = bin.inputBinName

        # bkg
        for bkgName in bkg_names:
            reader.openFile(inputDir,bkgName,TFileName)
            hist = reader.getObj(bkgName,histName)
            count,error = getIntegral(hist) 
            process = Process(bkgName,count if count >= 0. else 1e-12,error)
            bin.processList.append(process)

        # data
        dataCount = 0.
        for sample in data_names:
            reader.openFile(inputDir,sample,TFileName)
            hist = reader.getObj(sample,histName)
            count,error = getIntegral(hist)
            dataCount += count
        error = math.sqrt(dataCount)
        bin.data = Process("data_obs",int(dataCount),error)
        
        # signal
        hist = reader.getObj(signal_model_name,histName)
        count,error = getIntegral(hist)
        bin.processList.append(Process(signal_model_name,count if count >= 0. else 1e-12,error))
        
        # systematics
        bin.systList = []
        if count:
            mcSyst = lnNSystematic("SigStat_"+bin.name,[ signal_model_name, ],lambda syst,procName,anaBin: float(1.+error/count))
            #bin.systList.append(copy.deepcopy(mcSyst))
        for syst in commonLnSystematics:
            bin.systList.append(copy.deepcopy(syst))
        bin.systList += lnSystReader.makeLnSyst(bin.sysFile)
        if option.parametric:
            shapeFilePath = os.path.join(cardDir,"shape_"+bin.name+".root")
            outputFile = ROOT.TFile(shapeFilePath,"RECREATE")
            wsName = "parametric_pdf_"+bin.name
            w = ROOT.RooWorkspace(wsName,wsName)
            for sample,config in parameterDict.iteritems():
                inputShapeFile = ROOT.TFile(os.path.join(inputDir,sample,TFileName),"READ")
                hist = inputShapeFile.Get(bin.inputBinName)
                hist.Rebin(config.rebinFactor)
                if config.histFunc: config.histFunc(hist)
                if config.pdfType == pdfType_hist:
                    #pdf,dataHist,argSet = fitter.makeRooHistPdf("Pdf_"+sample,hist)
                    pdf,dataHist,argSet = fitter.makeRooHistPdf(sample,hist)
                elif config.pdfType == pdfType_data:
                    pdf = ROOT.RooDataHist("data_obs","",ROOT.RooArgList(fitter.obsVar),hist)
                elif config.pdfType in [pdfType_BW,pdfType_poly,pdfType_landau]:
                    if config.pdfType == pdfType_BW:
                        pdf,meanVar,widthVar = fitter.makeBreitWignerPdf(*config.pdfInput)
                    elif config.pdfType == pdfType_poly:
                        pdf = fitter.makePolyPdf(*config.pdfInput)
                    elif config.pdfType == pdfType_landau:
                        pdf,meanVar,widthVar = fitter.makeLandauPdf(*config.pdfInput)
                    config.evtYield = ROOT.RooRealVar("Yield","Yield", 0, 10000)
                    config.data = ROOT.RooDataHist("MCData_"+sample,"",ROOT.RooArgList(fitter.obsVar,config.evtYield),hist)
                    result = pdf.fitTo(config.data)
                    if option.drawDir:
                        if not os.path.exists(os.path.abspath(option.drawDir)):
                            os.makedirs(os.path.abspath(option.drawDir))
                        c = ROOT.TCanvas("c1","c1",800,800)
                        c.cd()
                        plot = fitter.obsVar.frame()
                        config.data.plotOn(plot,ROOT.RooFit.Name("data"))
                        pdf.plotOn(plot,ROOT.RooFit.Name("Parametric"))
                        plot.Draw()
                        c.SaveAs(option.drawDir+bin.name+"_"+sample+".pdf")
                getattr(w,'import')(pdf)
            outputFile.cd()
            w.Write()
            outputFile.Close()
            inputShapeFile.Close()
       
    dataCard.makeCard(cardDir,binListCopy)
    reader.end()
