import os,copy,math,argparse,ROOT

from StatFW.DataCard import DataCard,CardConfig
from StatFW.Systematic import *
from StatFW.Process import *
from StatFW.Reader import *
from StatFW.Channel import Bin
from StatFW.FileReader import FileReader
from StatFW.RateParameter import RateParameter

from Utilities.Hist import getCountAndError,getIntegral
from Utilities.DataCard import SignalModel
from Utilities.mkdir_p import mkdir_p

from Parametric.InputParameters_Mu import parameterDict_Mu
from Parametric.InputParameters_El import parameterDict_El
from Parametric.ShapeFitConfig import pdfType_hist,pdfType_BW,pdfType_poly,pdfType_landau,pdfType_data,pdfType_dcb
from Parametric.ShapeFitter import ShapeFitter

from StatFW.BaseObject import BaseObject

ROOT.gROOT.ProcessLine("gErrorIgnoreLevel = 1001;")

# ____________________________________________________________________________________________________________________________________________ ||
parser = argparse.ArgumentParser()
parser.add_argument("--inputDir",action="store")
parser.add_argument("--outputDir",action="store")
parser.add_argument("--verbose",action="store_true")
parser.add_argument("--elWidth",action="store",type=float,default=0.05)
parser.add_argument("--muWidth",action="store",type=float,default=0.02)
parser.add_argument("--systTextFile",action="store")
parser.add_argument("--interpolPath",action="store",default=None)
parser.add_argument("--zxShapeDir",action="store")

option = parser.parse_args()

# ____________________________________________________________________________________________________________________________________________ ||
# Configurable
inputDir = option.inputDir
if option.systTextFile:
    tf1,tf2,tf3,tf4,tf5 = option.systTextFile.split(",")
    commonLnSystFilePath = tf1
    lnSystFilePathDict = {
            #"TwoMu": tf2, 
            #"TwoEl": tf3, 
            "MuMu": tf2,
            "ElMu": tf3,
            "ElEl": tf4,
            "MuEl": tf5,
            }

outputDir = option.outputDir
TFileName = "StatInput.root"
epsilon_name = "epsilon"
init_epsilon = 0.05
isSRFunc = lambda x: x.name.endswith("SR")

interpolate_path = option.interpolPath

#mass_points = range(4,35)
#mass_points = [4,7,10,15,20,25,30]
mass_points     = [4.04*1.005**i for i in range(434)]

# ____________________________________________________________________________________________________________________________________________ ||
# mass window
signal_models = [ 
        #SignalModel("Zd_MZD"+str(m),["HZZd_M"+str(m),"ppZZd4l_M"+str(m)],m) for m in mass_points 
        SignalModel("Zd_MZD"+str(m),["HZZd_M"+str(m),],m) for m in mass_points 
        ]

bkgs = [
        BaseObject("Higgs"),
        BaseObject("qqZZ"),
        BaseObject("ggZZ"),
        BaseObject("ZPlusX",
            inputDir=option.zxShapeDir,
            TFileName="ParaShape.root",
            )
        ]

# ____________________________________________________________________________________________________________________________________________ ||
# bin list
binList_Mu = [
        Bin("MuMu_HiggsSR_SR",signalNames=["HZZd",],sysFile=lnSystFilePathDict["MuMu"],inputBinName="MuMu_HiggsSR",width=option.muWidth),
        Bin("MuMu_HiggsSR_SB",signalNames=["HZZd",],sysFile=lnSystFilePathDict["MuMu"],inputBinName="MuMu_HiggsSR",width=option.muWidth),
        Bin("ElMu_HiggsSR_SR",signalNames=["HZZd",],sysFile=lnSystFilePathDict["MuEl"],inputBinName="ElMu_HiggsSR",width=option.muWidth),
        Bin("ElMu_HiggsSR_SB",signalNames=["HZZd",],sysFile=lnSystFilePathDict["MuEl"],inputBinName="ElMu_HiggsSR",width=option.muWidth),
        ]

binList_El = [
        Bin("ElEl_HiggsSR_SR",signalNames=["HZZd",],sysFile=lnSystFilePathDict["ElEl"],inputBinName="ElEl_HiggsSR",width=option.elWidth),
        Bin("ElEl_HiggsSR_SB",signalNames=["HZZd",],sysFile=lnSystFilePathDict["ElEl"],inputBinName="ElEl_HiggsSR",width=option.elWidth),
        Bin("MuEl_HiggsSR_SR",signalNames=["HZZd",],sysFile=lnSystFilePathDict["MuEl"],inputBinName="MuEl_HiggsSR",width=option.elWidth),
        Bin("MuEl_HiggsSR_SB",signalNames=["HZZd",],sysFile=lnSystFilePathDict["MuEl"],inputBinName="MuEl_HiggsSR",width=option.elWidth),
        ]
if option.muOnly:
    binList = binList_Mu
elif option.elOnly:
    binList = binList_El
else:
    binList = binList_Mu + binList_El

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
    cardDir = os.path.join(outputDir,signal_model_name)
    mkdir_p(cardDir)
    for ibin,bin in enumerate(binListCopy):
        if option.verbose: print "-"*20
        if option.verbose: print bin.name
        histName = bin.inputBinName

        # bkg
        spb_data_count = 0.
        for bkg in bkgs:
            bkgName = bkg.name
            reader.openFile(inputDir if not hasattr(bkg,"inputDir") else bkg.inputDir,bkgName,TFileName if not hasattr(bkg,"TFileName") else bkg.TFileName)
            hist = reader.getObj(bkgName,histName)
            if bin.parameterDict:
                count,error = getIntegral(hist)
            else:
                count,error = getCountAndError(hist,central_value if not bin.central_value else bin.central_value,bin.width,isSR=isSRFunc(bin))
            process = Process(bkgName,count if count >= 0. else 1e-12,error)
            spb_data_count += count
            bin.processList.append(process)
        
        bin.systList = []
        
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

            outputFile.cd()
            w.Write()
            outputFile.Close()
            inputShapeFile.Close()

        reader.end()
