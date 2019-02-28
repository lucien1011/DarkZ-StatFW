import os,copy,math,argparse,ROOT

from StatFW.DataCard import DataCard,CardConfig
from StatFW.Systematic import *
from StatFW.Process import *
from StatFW.Reader import *
from StatFW.Channel import Bin
from StatFW.FileReader import FileReader
from StatFW.RateParameter import RateParameter

from Dataset.MergeSampleDict import mergeSampleDict

from Parametric.InputParameters_Mu import parameterDict_Mu
from Parametric.InputParameters_El import parameterDict_El
from Parametric.ShapeFitConfig import pdfType_hist,pdfType_BW,pdfType_poly,pdfType_landau,pdfType_data,pdfType_dcb
from Parametric.ShapeFitter import ShapeFitter

shapeStr = "shapes * * FAKE\n"

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
            0,
            hist.GetNbinsX()+1,
            #1,
            #hist.GetNbinsX(),
            error,
            )
    return integral,error
# ____________________________________________________________________________________________________________________________________________ ||
parser = argparse.ArgumentParser()
parser.add_argument("--inputDir",action="store")
parser.add_argument("--outputDir",action="store")
parser.add_argument("--verbose",action="store_true")
parser.add_argument("--parametric",action="store_true")
parser.add_argument("--rateParamOnHiggs",action="store_true")
parser.add_argument("--drawDir",action="store")
parser.add_argument("--drawLog",action="store_true")

option = parser.parse_args()

# ____________________________________________________________________________________________________________________________________________ ||
# Configurable
inputDir = option.inputDir
if option.rateParamOnHiggs:
    commonLnSystFilePath = "/home/lucien/Higgs/DarkZ/DarkZ-StatFW/Config/CommonSyst_2mu2e.txt"
else:
    commonLnSystFilePath = "/home/lucien/Higgs/DarkZ/DarkZ-StatFW/Config/CommonSyst_2mu2e_HiggsSyst.txt"
lnSystFilePathDict = {
        "FourEl": "/home/lucien/Higgs/DarkZ/DarkZ-StatFW/Config/Syst_4e.txt", 
        "FourMu": "/home/lucien/Higgs/DarkZ/DarkZ-StatFW/Config/Syst_4mu.txt", 
        "TwoElTwoMu": "/home/lucien/Higgs/DarkZ/DarkZ-StatFW/Config/Syst_2e2mu.txt", 
        "TwoMuTwoEl": "/home/lucien/Higgs/DarkZ/DarkZ-StatFW/Config/Syst_2mu2e.txt", 
        }
outputDir = option.outputDir
TFileName = "StatInput.root"

# ____________________________________________________________________________________________________________________________________________ ||
# mass window
signal_model_names = [
        #"HToZdZd_MZD15",
        "HToZdZd_MZD30",
        "HToZdZd_MZD50",
        "HToZdZd_MZD60",
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
        Bin("FourEl",signalName="HToZdZd",sysFile=lnSystFilePathDict["FourEl"],inputBinName="4e",width=0.05),
        Bin("FourMu",signalName="HToZdZd",sysFile=lnSystFilePathDict["FourMu"],inputBinName="4mu",width=0.02),
        Bin("TwoElTwoMu",signalName="HToZdZd",sysFile=lnSystFilePathDict["TwoElTwoMu"],inputBinName="2e2mu",width=0.02),
        Bin("TwoMuTwoEl",signalName="HToZdZd",sysFile=lnSystFilePathDict["TwoMuTwoEl"],inputBinName="2mu2e",width=0.05), 
        #Bin("FourEl",signalName="HToZdZd",sysFile=lnSystFilePathDict["FourEl"],inputBinName="4e",width=0.02),
        #Bin("FourMu",signalName="HToZdZd",sysFile=lnSystFilePathDict["FourMu"],inputBinName="4mu",width=0.01),
        #Bin("TwoElTwoMu",signalName="HToZdZd",sysFile=lnSystFilePathDict["TwoElTwoMu"],inputBinName="2e2mu",width=0.01),
        #Bin("TwoMuTwoEl",signalName="HToZdZd",sysFile=lnSystFilePathDict["TwoMuTwoEl"],inputBinName="2mu2e",width=0.02),
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

    central_value = float(signal_model_name.replace("HToZdZd_MZD",""))
    binListCopy = copy.deepcopy(binList)
    for ibin,bin in enumerate(binListCopy):
        if option.verbose: print "-"*20
        if option.verbose: print bin.name
        histName = bin.inputBinName

        bin.systList = []

        # bkg
        for bkgName in bkg_names:
            reader.openFile(inputDir,bkgName,TFileName)
            hist = reader.getObj(bkgName,histName)
            #count,error = getIntegral(hist) 
            count,error = getCountAndError(hist,central_value,central_value*bin.width,True)
            process = Process(bkgName,count if count >= 0. else 1e-12,error)
            bin.processList.append(process)
            if count and "ZPlusX" not in bkgName and "ggZZ" not in bkgName:
                #mcSyst = lnNSystematic(bkgName+"Stat_"+bin.name,[ bkgName, ],lambda syst,procName,anaBin: float(1.+error/count))
                mcSyst = lnNSystematic(bkgName+"Stat_"+bin.name,[ bkgName, ],magnitude=float(1.+error/count))
                bin.systList.append(copy.deepcopy(mcSyst))

        # data
        dataCount = 0.
        for sample in data_names:
            reader.openFile(inputDir,sample,TFileName)
            hist = reader.getObj(sample,histName)
            #count,error = getIntegral(hist)
            count,error = getCountAndError(hist,central_value,central_value*bin.width,True)
            dataCount += count
        error = math.sqrt(dataCount)
        bin.data = Process("data_obs",int(dataCount),error)
        
        # signal
        hist = reader.getObj(signal_model_name,histName)
        #count,error = getIntegral(hist)
        count,error = getCountAndError(hist,central_value,central_value*bin.width,True)
        bin.processList.append(Process(signal_model_name,count if count >= 0. else 1e-12,error))
        
        # systematics
        if count:
            mcSyst = lnNSystematic("SigStat_"+bin.name,[ signal_model_name, ],magnitude=float(1.+error/count))
            bin.systList.append(copy.deepcopy(mcSyst))
        for syst in commonLnSystematics:
            bin.systList.append(copy.deepcopy(syst))
        bin.systList += lnSystReader.makeLnSyst(bin.sysFile)

        if option.rateParamOnHiggs:
            if not ibin:
                rate_param_name = "HiggsRate"
                sm_higgs_rate_param = RateParameter(rate_param_name,"Higgs","1.","[0,20]")
            else:
                sm_higgs_rate_param = RateParameter(rate_param_name+"_"+bin.name,"Higgs","(@0)",rate_param_name)
            bin.rateParams.append(sm_higgs_rate_param)
        
        if option.parametric:
            shapeFilePath = os.path.join(cardDir,"shape_"+bin.name+".root")
            outputFile = ROOT.TFile(shapeFilePath,"RECREATE")
            wsName = "parametric_pdf_"+bin.name
            w = ROOT.RooWorkspace(wsName,wsName)
            for sample,config in bin.parameterDict.iteritems():
                if (sample not in bkg_names and sample not in data_names) and sample != signal_model_name: continue
                inputShapeFile = ROOT.TFile(os.path.join(inputDir,sample,TFileName),"READ")
                hist = inputShapeFile.Get(bin.inputBinName)
                hist.Rebin(config.rebinFactor)
                if config.histFunc: config.histFunc(hist)
                if config.pdfType == pdfType_hist:
                    pdf,dataHist,argSet = fitter.makeRooHistPdf(sample,hist)
                elif config.pdfType == pdfType_data:
                    #hist.Rebin(int(1./bin.parameterDict[signal_model_name].widthDict[bin.name]))
                    #hist.Rebin(int(1./bin.parameterDict[signal_model_name].widthDict[bin.name]*hist.GetNbinsX()))
                    pdf = ROOT.RooDataHist("data_obs","",ROOT.RooArgList(fitter.obsVar),hist)
                elif config.pdfType in [pdfType_BW,pdfType_poly,pdfType_landau,pdfType_dcb]:
                    if config.pdfType == pdfType_BW:
                        #hist.Rebin(int(1./bin.parameterDict[signal_model_name].widthDict[bin.name]))
                        pdf,meanVar,widthVar = fitter.makeBreitWignerPdf(*config.pdfInput)
                    elif config.pdfType == pdfType_poly:
                        pdf = fitter.makePolyPdf(*config.pdfInput)
                    elif config.pdfType == pdfType_landau:
                        pdf,meanVar,widthVar = fitter.makeLandauPdf(*config.pdfInput)
                    elif config.pdfType == pdfType_dcb:
                        pdf,meanVar,widthVar,alphaLVar,alphaRVar,nLVar,nRVar = fitter.makeDoubleCBPdf(*config.pdfInput)
                    config.evtYield = ROOT.RooRealVar("Yield","Yield", 0.01, 10000)
                    config.data = ROOT.RooDataHist("MCData_"+sample,"",ROOT.RooArgList(fitter.obsVar,config.evtYield),hist)
                    result = pdf.fitTo(config.data)
                    if option.drawDir:
                        if not os.path.exists(os.path.abspath(option.drawDir)):
                            os.makedirs(os.path.abspath(option.drawDir))
                        c = ROOT.TCanvas("c1","c1",800,800)
                        if option.drawLog:
                            c.SetLogy()
                        c.cd()
                        plot = fitter.obsVar.frame()
                        config.data.plotOn(plot,ROOT.RooFit.Name("data"))
                        pdf.plotOn(plot,ROOT.RooFit.Name("Parametric"))
                        if option.drawLog:
                            plot.SetMinimum(1E-5)
                            plot.SetMaximum(1E2)
                        plot.Draw()
                        c.SaveAs(option.drawDir+bin.name+"_"+sample+".pdf")
                getattr(w,'import')(pdf)
            outputFile.cd()
            w.Write()
            outputFile.Close()
            inputShapeFile.Close()
       
    dataCard.makeCard(cardDir,binListCopy)
    reader.end()
