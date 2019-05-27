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

# ____________________________________________________________________________________________________________________________________________ ||
parser = argparse.ArgumentParser()
parser.add_argument("--inputDir",action="store")
parser.add_argument("--outputDir",action="store")
parser.add_argument("--verbose",action="store_true")
parser.add_argument("--sideband",action="store_true")
parser.add_argument("--epsilon",action="store_true")
parser.add_argument("--elWidth",action="store",type=float,default=0.05)
parser.add_argument("--muWidth",action="store",type=float,default=0.02)

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
epsilon_name = "epsilon"
init_epsilon = 0.05
isSRFunc = lambda x: x.name.endswith("SR")
interpolate_path = "/home/lucien/public_html/Higgs/DarkZ/Interpolation/HZZd/2019-05-23_FirstVersion/"
mass_points = range(4,35)
#interpolate_path = None
#mass_points = [4,7,10,15,20,25,30] 

# ____________________________________________________________________________________________________________________________________________ ||
# mass window
signal_models = [ 
        #SignalModel("Zd_MZD"+str(m),["HZZd_M"+str(m),"ppZZd4l_M"+str(m)],m) for m in mass_points 
        SignalModel("Zd_MZD"+str(m),["HZZd_M"+str(m),],m) for m in mass_points 
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
        Bin("TwoEl_HiggsSR_SR",signalNames=["HZZd","ppZZd",],sysFile=lnSystFilePathDict["TwoEl"],inputBinName="2e_HiggsSR",width=option.elWidth),
        Bin("TwoMu_HiggsSR_SR",signalNames=["HZZd","ppZZd",],sysFile=lnSystFilePathDict["TwoMu"],inputBinName="2mu_HiggsSR",width=option.muWidth),
        Bin("TwoEl_HiggsSR_SB",signalNames=["HZZd","ppZZd",],sysFile=lnSystFilePathDict["TwoEl"],inputBinName="2e_HiggsSR",width=option.elWidth),
        Bin("TwoMu_HiggsSR_SB",signalNames=["HZZd","ppZZd",],sysFile=lnSystFilePathDict["TwoMu"],inputBinName="2mu_HiggsSR",width=option.muWidth),
        
        #Bin("TwoEl_HiggsSB_SR",signalNames=["HZZd","ppZZd",],sysFile=lnSystFilePathDict["TwoEl"],inputBinName="2e_HiggsSB",width=option.elWidth),
        #Bin("TwoMu_HiggsSB_SR",signalNames=["HZZd","ppZZd",],sysFile=lnSystFilePathDict["TwoMu"],inputBinName="2mu_HiggsSB",width=option.muWidth),
        #Bin("TwoEl_HiggsSB_SB",signalNames=["HZZd","ppZZd",],sysFile=lnSystFilePathDict["TwoEl"],inputBinName="2e_HiggsSB",width=option.elWidth),
        #Bin("TwoMu_HiggsSB_SB",signalNames=["HZZd","ppZZd",],sysFile=lnSystFilePathDict["TwoMu"],inputBinName="2mu_HiggsSB",width=option.muWidth),

        Bin("TwoEl_HiggsLowSB_SR",signalNames=["HZZd","ppZZd",],sysFile=lnSystFilePathDict["TwoEl"],inputBinName="2e_HiggsLowSB",width=option.elWidth),
        Bin("TwoMu_HiggsLowSB_SR",signalNames=["HZZd","ppZZd",],sysFile=lnSystFilePathDict["TwoMu"],inputBinName="2mu_HiggsLowSB",width=option.muWidth),
        Bin("TwoEl_HiggsLowSB_SB",signalNames=["HZZd","ppZZd",],sysFile=lnSystFilePathDict["TwoEl"],inputBinName="2e_HiggsLowSB",width=option.elWidth),
        Bin("TwoMu_HiggsLowSB_SB",signalNames=["HZZd","ppZZd",],sysFile=lnSystFilePathDict["TwoMu"],inputBinName="2mu_HiggsLowSB",width=option.muWidth),

        Bin("TwoEl_HiggsHighSB_SR",signalNames=["HZZd","ppZZd",],sysFile=lnSystFilePathDict["TwoEl"],inputBinName="2e_HiggsHighSB",width=option.elWidth),
        Bin("TwoMu_HiggsHighSB_SR",signalNames=["HZZd","ppZZd",],sysFile=lnSystFilePathDict["TwoMu"],inputBinName="2mu_HiggsHighSB",width=option.muWidth),
        Bin("TwoEl_HiggsHighSB_SB",signalNames=["HZZd","ppZZd",],sysFile=lnSystFilePathDict["TwoEl"],inputBinName="2e_HiggsHighSB",width=option.elWidth),
        Bin("TwoMu_HiggsHighSB_SB",signalNames=["HZZd","ppZZd",],sysFile=lnSystFilePathDict["TwoMu"],inputBinName="2mu_HiggsHighSB",width=option.muWidth),
        ]

if interpolate_path:
    for b in binList:
        if not b.name.endswith("_SR"): continue
        b.interFuncDict = {}
        b.interFileDict = {}
        b.interFileDict["ppZZd4l"] = ROOT.TFile(os.path.join(interpolate_path,"ppZZd",b.inputBinName+".root"),"READ")
        b.interFuncDict["ppZZd4l"] = b.interFileDict["ppZZd4l"].Get(b.inputBinName+"_fitFunc")
        b.interFileDict["HZZd"] = ROOT.TFile(os.path.join(interpolate_path,"HZZd",b.inputBinName+".root"),"READ")
        b.interFuncDict["HZZd"] = b.interFileDict["HZZd"].Get(b.inputBinName+"_fitFunc")

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
    #central_value = float(signal_model_name.replace("HZZd_M",""))
    central_value = signal_model.central_value
    binListCopy = [b for b in copy.deepcopy(binList) if option.sideband or (not option.sideband and "SR" in b.name)]
    for ibin,bin in enumerate(binListCopy):
        if option.verbose: print "-"*20
        if option.verbose: print bin.name
        histName = bin.inputBinName

        # bkg
        for bkgName in bkg_names:
            reader.openFile(inputDir,bkgName,TFileName)
            hist = reader.getObj(bkgName,histName)
            count,error = getCountAndError(hist,central_value,bin.width,isSR=isSRFunc(bin))
            process = Process(bkgName,count if count >= 0. else 1e-12,error)
            bin.processList.append(process)

        # data
        dataCount = 0.
        for sample in data_names:
            reader.openFile(inputDir,sample,TFileName)
            hist = reader.getObj(sample,histName)
            count,error = getCountAndError(hist,central_value,bin.width,isSR=isSRFunc(bin))
            dataCount += count
        error = math.sqrt(dataCount)
        bin.data = Process("data_obs",int(dataCount),error)
        
        bin.systList = []
        
        # signal
        for each_signal_model_name in signal_model.signal_list:
            if not interpolate_path:
                reader.openFile(inputDir,each_signal_model_name,TFileName)
                hist = reader.getObj(each_signal_model_name,histName)
                count,error = copy.deepcopy(getCountAndError(hist,central_value,bin.width,isSR=isSRFunc(bin)))
                bin.processList.append(Process(each_signal_model_name,count if count >= 0. else 1e-12,error))
                
                # systematics
                if count:
                    mcSyst = lnNSystematic("SigStat_"+bin.name,[ each_signal_model_name, ],lambda syst,procName,anaBin: float(1.+error/count))
                    #bin.systList.append(copy.deepcopy(mcSyst))
            else:
                if bin.name.endswith("_SR"): 
                    for key in bin.interFuncDict:
                        if key in each_signal_model_name: break
                    count = bin.interFuncDict[key].Eval(central_value)
                else:
                    count = 0.
                bin.processList.append(Process(each_signal_model_name,count if count > 0. else 1e-12,0.))
        
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

        if option.epsilon:
            eps_rate_param_name = "EpsilonRate_"+bin.name
            for each_signal_model_name in signal_model.signal_list:
                if "ppZZd" in each_signal_model_name:
                    #eps_power = 4
                    eps_power = 2
                else:
                    eps_power = 2
                bin.rateParams.append(RateParameter(eps_rate_param_name,each_signal_model_name,"(@0)^"+str(eps_power)+"/"+str(init_epsilon)+"^"+str(eps_power),epsilon_name))

    if option.epsilon:
        bin.parameterList = [epsilon_name,]
        bin.paramDict = {
                epsilon_name: [epsilon_name,"0.02","0.002.","[-5,5]"],
                }

    config = CardConfig(signal_model_name)
    dataCard = DataCard(config) 
    cardDir = outputDir+"/"+dataCard.makeOutFileName("/","")
    mkdir_p(cardDir)
    dataCard.makeCard(cardDir,binListCopy)
    reader.end()
