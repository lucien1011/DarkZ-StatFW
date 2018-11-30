import os,copy,math,argparse,ROOT

from StatFW.DataCard import DataCard,CardConfig
from StatFW.Systematic import *
from StatFW.Process import *
from StatFW.Reader import *
from StatFW.Channel import Bin
from StatFW.FileReader import FileReader
from StatFW.RateParameter import RateParameter

from Dataset.MergeSampleDict import mergeSampleDict

def getCountAndError(hist,central,width,isSR=True):
    lower_value = central*(1.-width)
    upper_value = central*(1.+width)

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

# ____________________________________________________________________________________________________________________________________________ ||
parser = argparse.ArgumentParser()
parser.add_argument("--inputDir",action="store")
parser.add_argument("--outputDir",action="store")
parser.add_argument("--verbose",action="store_true")
parser.add_argument("--sideband",action="store_true")

option = parser.parse_args()

# ____________________________________________________________________________________________________________________________________________ ||
# Configurable
inputDir = option.inputDir
if option.sideband:
    commonLnSystFilePath = "/home/lucien/Higgs/DarkZ/DarkZ-StatFW/Config/CommonSyst_2mu2e.txt"
else:
    commonLnSystFilePath = "/home/lucien/Higgs/DarkZ/DarkZ-StatFW/Config/CommonSyst_2mu2e_HiggsSyst.txt"
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
        "HZZd_M10",  
        "HZZd_M15",  
        "HZZd_M20",  
        "HZZd_M25",  
        "HZZd_M30",  
        "HZZd_M4", 
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
        Bin("TwoEl_SR",sysFile=lnSystFilePathDict["TwoEl"],inputBinName="2e",width=0.05),
        Bin("TwoMu_SR",sysFile=lnSystFilePathDict["TwoMu"],inputBinName="2mu",width=0.02),
        Bin("TwoEl_SB",sysFile=lnSystFilePathDict["TwoEl"],inputBinName="2e",width=0.05),
        Bin("TwoMu_SB",sysFile=lnSystFilePathDict["TwoMu"],inputBinName="2mu",width=0.02),
        ]

# ____________________________________________________________________________________________________________________________________________ ||
# syst
lnSystReader = LogNormalSystReader()
commonLnSystematics = lnSystReader.makeLnSyst(commonLnSystFilePath)

# ____________________________________________________________________________________________________________________________________________ ||
reader = FileReader()

if not os.path.exists(os.path.abspath(outputDir)):
    os.makedirs(os.path.abspath(outputDir))

for signal_model_name in signal_model_names:
    reader.openFile(inputDir,signal_model_name,TFileName)
    if option.verbose: print "*"*100
    if option.verbose: print "Making data card for ",signal_model_name
    central_value = float(signal_model_name.replace("HZZd_M",""))
    binListCopy = [b for b in copy.deepcopy(binList) if option.sideband or (not option.sideband and "SR" in b.name)]
    for ibin,bin in enumerate(binListCopy):
        if option.verbose: print "-"*20
        if option.verbose: print bin.name
        histName = bin.inputBinName

        # bkg
        for bkgName in bkg_names:
            reader.openFile(inputDir,bkgName,TFileName)
            hist = reader.getObj(bkgName,histName)
            count,error = getCountAndError(hist,central_value,bin.width,isSR="SR" in bin.name)
            process = Process(bkgName,count if count >= 0. else 1e-12,error)
            bin.processList.append(process)

        # data
        dataCount = 0.
        for sample in data_names:
            reader.openFile(inputDir,sample,TFileName)
            hist = reader.getObj(sample,histName)
            count,error = getCountAndError(hist,central_value,bin.width,isSR="SR" in bin.name)
            dataCount += count
        error = math.sqrt(dataCount)
        bin.data = Process("data_obs",int(dataCount),error)
        
        # signal
        hist = reader.getObj(signal_model_name,histName)
        count,error = copy.deepcopy(getCountAndError(hist,central_value,bin.width,isSR="SR" in bin.name))
        bin.processList.append(Process(signal_model_name,count if count >= 0. else 1e-12,error))
        
        # systematics
        bin.systList = []
        if count:
            mcSyst = lnNSystematic("SigStat_"+bin.name,[ signal_model_name, ],lambda syst,procName,anaBin: float(1.+error/count))
            #bin.systList.append(copy.deepcopy(mcSyst))
        for syst in commonLnSystematics:
            bin.systList.append(copy.deepcopy(syst))
        bin.systList += lnSystReader.makeLnSyst(bin.sysFile)
       
        if option.sideband:
            if not ibin:
                rate_param_name = "HiggsRate"
                sm_higgs_rate_param = RateParameter(rate_param_name,"Higgs","1.","[0,20]")
            else:
                sm_higgs_rate_param = RateParameter(rate_param_name+"_"+bin.name,"Higgs","(@0)",rate_param_name)
            bin.rateParams.append(sm_higgs_rate_param)

    config = CardConfig(signal_model_name)
    dataCard = DataCard(config) 
    cardDir = outputDir+"/"+dataCard.makeOutFileName("/","")
    if not os.path.exists(os.path.abspath(cardDir)):
        os.makedirs(os.path.abspath(cardDir))
    dataCard.makeCard(cardDir,binListCopy)
    reader.end()
