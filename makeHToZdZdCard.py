import os,copy,math,argparse,ROOT

from StatFW.DataCard import DataCard,CardConfig
from StatFW.Systematic import *
from StatFW.Process import *
from StatFW.Reader import *
from StatFW.Channel import Bin
from StatFW.FileReader import FileReader
from StatFW.RateParameter import RateParameter

from Utils.Hist import getCountAndError,getIntegral
from Utils.DataCard import SignalModel
from Utils.mkdir_p import mkdir_p

shapeStr = "shapes * * FAKE\n"

# ____________________________________________________________________________________________________________________________________________ ||
parser = argparse.ArgumentParser()
parser.add_argument("--inputDir",action="store")
parser.add_argument("--outputDir",action="store")
parser.add_argument("--verbose",action="store_true")
parser.add_argument("--rateParamOnHiggs",action="store_true")
parser.add_argument("--elWidth",action="store",type=float,default=0.05)
parser.add_argument("--muWidth",action="store",type=float,default=0.02)
parser.add_argument("--massRatio",action="store",type=float,default=0.)
parser.add_argument("--systTextFile",action="store")
parser.add_argument("--appendToPath",action="store")

option = parser.parse_args()

# ____________________________________________________________________________________________________________________________________________ ||
# Configurable
inputDir = option.inputDir
if option.systTextFile:
    tf1,tf2 = option.systTextFile.split(",")
    commonLnSystFilePath = tf1
    lnSystFilePathDict = {
            "TwoMu": tf2, 
            "TwoEl": tf2, 
            }
else:
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
signal_models = [
        SignalModel("Zd_MZD4",["HToZdZd_MZD4",],4.,),
        SignalModel("Zd_MZD5",["HToZdZd_MZD5",],5.,),
        SignalModel("Zd_MZD6",["HToZdZd_MZD6",],6.,),
        SignalModel("Zd_MZD7",["HToZdZd_MZD7",],7.,),
        SignalModel("Zd_MZD8",["HToZdZd_MZD8",],8.,),
        SignalModel("Zd_MZD9",["HToZdZd_MZD9",],9.,),
        SignalModel("Zd_MZD10",["HToZdZd_MZD10",],10.,),
        SignalModel("Zd_MZD15",["HToZdZd_MZD15",],15.,),
        SignalModel("Zd_MZD20",["HToZdZd_MZD20",],20.,),
        SignalModel("Zd_MZD25",["HToZdZd_MZD25",],25.,),
        SignalModel("Zd_MZD30",["HToZdZd_MZD30",],30.,),
        SignalModel("Zd_MZD35",["HToZdZd_MZD35",],35.,),
        SignalModel("Zd_MZD40",["HToZdZd_MZD40",],40.,),
        SignalModel("Zd_MZD45",["HToZdZd_MZD45",],45.,),
        SignalModel("Zd_MZD50",["HToZdZd_MZD50",],50.,),
        SignalModel("Zd_MZD55",["HToZdZd_MZD55",],55.,),
        SignalModel("Zd_MZD60",["HToZdZd_MZD60",],60.,),
        ]

data_names = [
        "Data",
        ]

bkg_names = [
        "Higgs",
        "qqZZ",
        "ggZZ",
        "ZPlusX",
        ]

# ____________________________________________________________________________________________________________________________________________ ||
# bin list
binList = [
        #Bin("FourEl",signalNames=["HToZdZd",],sysFile=lnSystFilePathDict["FourEl"],inputBinName="4e",width=option.elWidth),
        #Bin("TwoMuTwoEl",signalNames=["HToZdZd",],sysFile=lnSystFilePathDict["TwoMuTwoEl"],inputBinName="2mu2e",width=option.elWidth), 
        #Bin("FourMu",signalNames=["HToZdZd",],sysFile=lnSystFilePathDict["FourMu"],inputBinName="4mu",width=option.muWidth),
        #Bin("TwoElTwoMu",signalNames=["HToZdZd",],sysFile=lnSystFilePathDict["TwoElTwoMu"],inputBinName="2e2mu",width=option.muWidth),
        #Bin("FourEl",signalName="HToZdZd",sysFile=lnSystFilePathDict["FourEl"],inputBinName="4e",width=0.02),
        #Bin("FourMu",signalName="HToZdZd",sysFile=lnSystFilePathDict["FourMu"],inputBinName="4mu",width=0.01),
        #Bin("TwoElTwoMu",signalName="HToZdZd",sysFile=lnSystFilePathDict["TwoElTwoMu"],inputBinName="2e2mu",width=0.01),
        #Bin("TwoMuTwoEl",signalName="HToZdZd",sysFile=lnSystFilePathDict["TwoMuTwoEl"],inputBinName="2mu2e",width=0.02),

        Bin("TwoMu",signalNames=["HToZdZd",],sysFile=lnSystFilePathDict["TwoMu"],inputBinName="2mu" if not option.massRatio else "2mu_"+str(option.massRatio),width=option.muWidth), 
        Bin("TwoEl",signalNames=["HToZdZd",],sysFile=lnSystFilePathDict["TwoEl"],inputBinName="2e" if not option.massRatio else "2e_"+str(option.massRatio),width=option.elWidth), 
        ]

# ____________________________________________________________________________________________________________________________________________ ||
# syst
lnSystReader = LogNormalSystReader()
commonLnSystematics = lnSystReader.makeLnSyst(commonLnSystFilePath)

# ____________________________________________________________________________________________________________________________________________ ||
reader = FileReader()

if not os.path.exists(os.path.abspath(outputDir)):
    os.makedirs(os.path.abspath(outputDir))

for signal_model in signal_models:
    signal_model_name = signal_model.name
    if option.verbose: print "*"*100
    if option.verbose: print "Making data card for ",signal_model_name
    
    config = CardConfig(signal_model_name)
    config.shapeStr = shapeStr
    dataCard = DataCard(config) 
    cardDir = outputDir+"/"+dataCard.makeOutFileName("/","")
    if not os.path.exists(os.path.abspath(cardDir)):
        os.makedirs(os.path.abspath(cardDir))

    central_value = signal_model.central_value 
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
            process = Process(bkgName,count if count > 0. else 1e-6,error)
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
        for each_signal_model_name in signal_model.signal_list:
            reader.openFile(inputDir,each_signal_model_name,TFileName)
            hist = reader.getObj(each_signal_model_name,histName)
            #count,error = getIntegral(hist)
            count,error = getCountAndError(hist,central_value,central_value*bin.width,True)
            bin.processList.append(Process(each_signal_model_name,count if count > 0. else 1e-6,error))
        
        # systematics
            if count:
                mcSyst = lnNSystematic("SigStat_"+bin.name,[ each_signal_model_name, ],magnitude=float(1.+error/count))
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
 
    dataCard.makeCard(cardDir,binListCopy,appendToPath=option.appendToPath if option.appendToPath else "")
    reader.end()
