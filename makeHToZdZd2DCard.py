import os,copy,math,argparse,ROOT

from StatFW.DataCard import DataCard,CardConfig
from StatFW.Systematic import *
from StatFW.Process import *
from StatFW.Reader import *
from StatFW.Channel import Bin
from StatFW.FileReader import FileReader
from StatFW.RateParameter import RateParameter
from StatFW.BaseObject import BaseObject

from Utilities.Hist import getCountAndError2D,getCountAndError
from Utilities.DataCard import SignalModel
from Utilities.mkdir_p import mkdir_p

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
parser.add_argument("--interpolPath",action="store",default=None)
parser.add_argument("--zxShapeDir",action="store")
parser.add_argument("--muOnly",action="store_true")
parser.add_argument("--elOnly",action="store_true")

option = parser.parse_args()

# ____________________________________________________________________________________________________________________________________________ ||
# Configurable
inputDir = option.inputDir
if option.systTextFile:
    tf1,tf2,tf3,tf4,tf5 = option.systTextFile.split(",")
    #tf1,tf2,tf3 = option.systTextFile.split(",")
    commonLnSystFilePath = tf1
    lnSystFilePathDict = {
            #"Mu": tf2, 
            #"El": tf3, 
            "MuMu": tf2,
            "ElMu": tf3,
            "ElEl": tf4,
            "MuEl": tf5,
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
            #"TwoMu": "/home/lucien/Higgs/DarkZ/DarkZ-StatFW/Config/Syst_2mu.txt", 
            #"TwoEl": "/home/lucien/Higgs/DarkZ/DarkZ-StatFW/Config/Syst_2e.txt", 
            }
outputDir = option.outputDir
interpolate_path = option.interpolPath
TFileName = "StatInput.root"

# ____________________________________________________________________________________________________________________________________________ ||
# mass window
#mass_points = [4.04*1.005**i for i in range(551)]
mass_points = [4.20*1.005**i for i in range(541)]
#mass_points = [4,5,6,7,8,9,10,15,20,25,30,35,40,45,50,55,60]
signal_models = [
        SignalModel("Zd_MZD"+str(m),["HToZdZd_M"+str(m),],m,) for m in mass_points
        ]

data = [
        BaseObject("Data"),
        ]

bkgs = [
        BaseObject("Higgs"),
        #BaseObject("qqZZ"),
        #BaseObject("ggZZ"),
        BaseObject("ZZ"),
        BaseObject("WWZ"),
        BaseObject("ttZ"),
        BaseObject("ZPlusX",
            inputDir=option.zxShapeDir,
            TFileName="ParaShape.root",
            shapeFuncPostfix="_fitFunc",
            normHistPostfix="_norm",
            #countErrorFunc=getCountAndError
            )
        ]

# ____________________________________________________________________________________________________________________________________________ ||
# bin list
binList_MuMu = [
        Bin("MuMu",signalNames=["HToZdZd",],sysFile=lnSystFilePathDict["MuMu"],inputBinName="MuMu",x_width=option.muWidth,y_width=option.muWidth), 
        ]
binList_ElMu = [
        Bin("ElMu",signalNames=["HToZdZd",],sysFile=lnSystFilePathDict["ElMu"],inputBinName="ElMu",x_width=option.elWidth,y_width=option.muWidth), 
        Bin("MuEl",signalNames=["HToZdZd",],sysFile=lnSystFilePathDict["MuEl"],inputBinName="MuEl",x_width=option.muWidth,y_width=option.elWidth),
        ]
binList_ElEl = [
        Bin("ElEl",signalNames=["HToZdZd",],sysFile=lnSystFilePathDict["ElEl"],inputBinName="ElEl",x_width=option.elWidth,y_width=option.elWidth), 
        ]
if option.muOnly:
    binList = binList_MuMu
elif option.elOnly:
    binList = binList_ElEl
else:
    binList = binList_MuMu + binList_ElEl + binList_ElMu

if interpolate_path:
    for b in binList:
        b.interFuncDict = {}
        b.interFileDict = {}
        b.interFileDict["HToZdZd"] = ROOT.TFile(os.path.join(interpolate_path,b.inputBinName+"_pol5.root"),"READ")
        b.interFuncDict["HToZdZd"] = b.interFileDict["HToZdZd"].Get(b.inputBinName+"_fitFunc")

# ____________________________________________________________________________________________________________________________________________ ||
# syst
lnSystReader = LogNormalSystReader()
commonLnSystematics = lnSystReader.makeLnSyst(commonLnSystFilePath)

zero = 1e-12

# ____________________________________________________________________________________________________________________________________________ ||
reader = FileReader()

if not os.path.exists(os.path.abspath(outputDir)):
    os.makedirs(os.path.abspath(outputDir))

for signal_model in signal_models:
    signal_model_name = signal_model.name
    if option.verbose: print "*"*100
    if option.verbose: print "Making data card for ",signal_model_name,option.appendToPath
    
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
        for bkg in bkgs:
            bkgName = bkg.name
            reader.openFile(inputDir if not hasattr(bkg,"inputDir") else bkg.inputDir,bkgName,TFileName if not hasattr(bkg,"TFileName") else bkg.TFileName)
            hist = reader.getObj(bkgName,histName)
            if not hasattr(bkg,"shapeFuncPostfix") and not hasattr(bkg,"normHistPostfix"):
                count,error = getCountAndError2D(hist,central_value,bin.x_width,bin.y_width) 
            else:
                fitFunc = reader.getObj(bkgName,bin.inputBinName+bkg.shapeFuncPostfix)
                normHist = reader.getObj(bkgName,bin.inputBinName+bkg.normHistPostfix)
                normFactor = normHist.Integral() if normHist.Integral() >= 0. else 0.
                count = fitFunc.Eval(central_value)*normFactor
                error = 0.
            process = Process(bkgName,count if count > zero else zero,error)
            bin.processList.append(process)
            if count > 0. and "ZPlusX" not in bkgName:
                mcSyst = lnNSystematic("_".join([bkgName+"Stat",bin.name,option.appendToPath]),[ bkgName,],magnitude=float(1.+error/count))
                #if count < zero:
                #    gmnN = int((count/error)**2)
                #    gmnRate = zero/gmnN
                #else:
                #    gmnN = int((count/error)**2)
                #    gmnRate = count/gmnN
                #mcSyst = gmNSystematic("_".join([bkgName+"Stat",bin.name,option.appendToPath]),[ bkgName,],N=gmnN,rate=gmnRate)
                bin.systList.append(copy.deepcopy(mcSyst))
            elif "ZPlusX" == bkgName and count > zero:
                gmnN = int(normHist.GetEntries())
                if count > zero:
                    gmnRate = count/gmnN
                else:
                    gmnRate = zero/gmnN
                mcSyst = gmNSystematic("_".join([bkgName+"Stat",bin.name,option.appendToPath]),[ bkgName,],N=gmnN,rate=gmnRate)
                bin.systList.append(copy.deepcopy(mcSyst))

        # data
        dataCount = 0.
        for datum in data:
            sample = datum.name
            reader.openFile(inputDir,sample,TFileName)
            hist = reader.getObj(sample,histName)
            count,error = getCountAndError2D(hist,central_value,bin.x_width,bin.y_width)
            dataCount += count
        error = math.sqrt(dataCount)
        bin.data = Process("data_obs",int(dataCount),error)
        
        # signal
        for each_signal_model_name in signal_model.signal_list:
            if not interpolate_path:
                reader.openFile(inputDir,each_signal_model_name,TFileName)
                hist = reader.getObj(each_signal_model_name,histName)
                count,error = getCountAndError2D(hist,central_value,bin.x_width,bin.y_width)
                bin.processList.append(Process(each_signal_model_name,count if count > zero else zero,error))
                # systematics
                if count:
                    mcSyst = lnNSystematic("SigStat_"+bin.name,[ each_signal_model_name, ],magnitude=float(1.+error/count))
                    #mcSyst = gmNSystematic("SigStat_"+bin.name,[ each_signal_model_name, ],N=count,rate=1.)
                    bin.systList.append(copy.deepcopy(mcSyst))
            else:
                for key in bin.interFuncDict:
                    if key in each_signal_model_name: break
                count = bin.interFuncDict[key].Eval(central_value)
                bin.processList.append(Process(each_signal_model_name,count if count > zero else zero,0.))
     
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
