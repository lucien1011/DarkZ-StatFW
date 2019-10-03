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
parser.add_argument("--epsilon",action="store_true")
parser.add_argument("--parametric",action="store_true")
parser.add_argument("--sideband",action="store_true")
parser.add_argument("--elWidth",action="store",type=float,default=0.05)
parser.add_argument("--muWidth",action="store",type=float,default=0.02)
parser.add_argument("--drawDir",action="store")
parser.add_argument("--drawLog",action="store_true")
parser.add_argument("--appendToPath",action="store")
parser.add_argument("--systTextFile",action="store")
parser.add_argument("--interpolPath",action="store",default=None)
parser.add_argument("--setDataCountToMC",action="store_true")
parser.add_argument("--zxShapeDir",action="store")
parser.add_argument("--sigSF",action="store",type=float,default=1.)

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

data = [
        #"Data2016",
        BaseObject("Data"),
        ]

#bkg_names = mergeSampleDict.keys()
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
binList_SR = [
        #Bin("MuMu_HiggsSR_SR",signalNames=["HZZd","ppZZd",],sysFile=lnSystFilePathDict["MuMu"],inputBinName="MuMu_HiggsSR",width=option.muWidth),
        #Bin("MuMu_HiggsSR_SB",signalNames=["HZZd","ppZZd",],sysFile=lnSystFilePathDict["MuMu"],inputBinName="MuMu_HiggsSR",width=option.muWidth),
        #Bin("ElMu_HiggsSR_SR",signalNames=["HZZd","ppZZd",],sysFile=lnSystFilePathDict["ElMu"],inputBinName="ElMu_HiggsSR",width=option.muWidth),
        #Bin("ElMu_HiggsSR_SB",signalNames=["HZZd","ppZZd",],sysFile=lnSystFilePathDict["ElMu"],inputBinName="ElMu_HiggsSR",width=option.muWidth),
        Bin("ElEl_HiggsSR_SR",signalNames=["HZZd","ppZZd",],sysFile=lnSystFilePathDict["ElEl"],inputBinName="ElEl_HiggsSR",width=option.muWidth),
        Bin("ElEl_HiggsSR_SB",signalNames=["HZZd","ppZZd",],sysFile=lnSystFilePathDict["ElEl"],inputBinName="ElEl_HiggsSR",width=option.muWidth),
        Bin("MuEl_HiggsSR_SR",signalNames=["HZZd","ppZZd",],sysFile=lnSystFilePathDict["MuEl"],inputBinName="MuEl_HiggsSR",width=option.muWidth),
        Bin("MuEl_HiggsSR_SB",signalNames=["HZZd","ppZZd",],sysFile=lnSystFilePathDict["MuEl"],inputBinName="MuEl_HiggsSR",width=option.muWidth),
        ]

binList_LowSB = [
        Bin("MuMu_HiggsLowSB_SR",signalNames=["HZZd","ppZZd",],sysFile=lnSystFilePathDict["MuMu"],inputBinName="MuMu_HiggsLowSB",width=option.elWidth),
        Bin("MuMu_HiggsLowSB_SB",signalNames=["HZZd","ppZZd",],sysFile=lnSystFilePathDict["MuMu"],inputBinName="MuMu_HiggsLowSB",width=option.elWidth),
        Bin("ElMu_HiggsLowSB_SR",signalNames=["HZZd","ppZZd",],sysFile=lnSystFilePathDict["ElMu"],inputBinName="ElMu_HiggsLowSB",width=option.elWidth),
        Bin("ElMu_HiggsLowSB_SB",signalNames=["HZZd","ppZZd",],sysFile=lnSystFilePathDict["ElMu"],inputBinName="ElMu_HiggsLowSB",width=option.elWidth),
        Bin("ElEl_HiggsLowSB_SR",signalNames=["HZZd","ppZZd",],sysFile=lnSystFilePathDict["ElEl"],inputBinName="ElEl_HiggsLowSB",width=option.elWidth),
        Bin("ElEl_HiggsLowSB_SB",signalNames=["HZZd","ppZZd",],sysFile=lnSystFilePathDict["ElEl"],inputBinName="ElEl_HiggsLowSB",width=option.elWidth),
        Bin("MuEl_HiggsLowSB_SR",signalNames=["HZZd","ppZZd",],sysFile=lnSystFilePathDict["MuEl"],inputBinName="MuEl_HiggsLowSB",width=option.elWidth),
        Bin("MuEl_HiggsLowSB_SB",signalNames=["HZZd","ppZZd",],sysFile=lnSystFilePathDict["MuEl"],inputBinName="MuEl_HiggsLowSB",width=option.elWidth),
        ]

binList_HighSB = [
        Bin("MuMu_HiggsHighSB_SR",signalNames=["HZZd","ppZZd",],sysFile=lnSystFilePathDict["MuMu"],inputBinName="MuMu_HiggsHighSB",width=option.elWidth),
        Bin("MuMu_HiggsHighSB_SB",signalNames=["HZZd","ppZZd",],sysFile=lnSystFilePathDict["MuMu"],inputBinName="MuMu_HiggsHighSB",width=option.elWidth),
        Bin("ElMu_HiggsHighSB_SR",signalNames=["HZZd","ppZZd",],sysFile=lnSystFilePathDict["ElMu"],inputBinName="ElMu_HiggsHighSB",width=option.elWidth),
        Bin("ElMu_HiggsHighSB_SB",signalNames=["HZZd","ppZZd",],sysFile=lnSystFilePathDict["ElMu"],inputBinName="ElMu_HiggsHighSB",width=option.elWidth),
        Bin("ElEl_HiggsHighSB_SR",signalNames=["HZZd","ppZZd",],sysFile=lnSystFilePathDict["ElEl"],inputBinName="ElEl_HiggsHighSB",width=option.elWidth),
        Bin("ElEl_HiggsHighSB_SB",signalNames=["HZZd","ppZZd",],sysFile=lnSystFilePathDict["ElEl"],inputBinName="ElEl_HiggsHighSB",width=option.elWidth),
        Bin("MuEl_HiggsHighSB_SR",signalNames=["HZZd","ppZZd",],sysFile=lnSystFilePathDict["MuEl"],inputBinName="MuEl_HiggsHighSB",width=option.elWidth),
        Bin("MuEl_HiggsHighSB_SB",signalNames=["HZZd","ppZZd",],sysFile=lnSystFilePathDict["MuEl"],inputBinName="MuEl_HiggsHighSB",width=option.elWidth),
        ]

binList = binList_SR

# ____________________________________________________________________________________________________________________________________________ ||
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

if option.parametric:
    fitter = ShapeFitter("massZ2",0.,1.)
    #fitter = ShapeFitter("massZ2",4.,35.)
    
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
        config = CardConfig(bin.name)
        if bin.parameterDict:
            shapeStr = "shapes * TwoEl_HiggsSR_SR shape_TwoEl_HiggsSR_SR.root parametric_pdf_TwoEl_HiggsSR_SR:$PROCESS\n"
            shapeStr += "shapes * TwoMu_HiggsSR_SR shape_TwoMu_HiggsSR_SR.root parametric_pdf_TwoMu_HiggsSR_SR:$PROCESS\n"
        else:
            shapeStr = "shapes * * FAKE\n"
        if bin.parameterDict:
            config.shapeStr = shapeStr
        dataCard = DataCard(config) 

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
            process = Process(bkgName,count*option.sigSF if count >= 0. else 1e-12,error*option.sigSF)
            spb_data_count += count
            bin.processList.append(process)
        
        bin.systList = []
        
        # signal
        for each_signal_model_name in signal_model.signal_list:
            if not interpolate_path:
                reader.openFile(inputDir,each_signal_model_name,TFileName)
                hist = reader.getObj(each_signal_model_name,histName)
                if bin.parameterDict:
                    count,error = getIntegral(hist)
                else:
                    count,error = getCountAndError(hist,central_value if not bin.central_value else bin.central_value,bin.width,isSR=isSRFunc(bin))
                spb_data_count += count
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

        # data
        dataCount = 0.
        for datum in data:
            sample = datum.name
            reader.openFile(inputDir,sample,TFileName)
            hist = reader.getObj(sample,histName)
            if bin.parameterDict:
                count,error = getIntegral(hist)
            else:
                count,error = getCountAndError(hist,central_value if not bin.central_value else bin.central_value,bin.width,isSR=isSRFunc(bin))
            dataCount += count
        error = math.sqrt(dataCount)
        bin.data = Process("data_obs",int(dataCount) if not option.setDataCountToMC else int(spb_data_count),error)

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
        if bin.parameterDict:
            shapeFilePath = os.path.join(cardDir,"shape_"+bin.name+".root")
            outputFile = ROOT.TFile(shapeFilePath,"RECREATE")
            wsName = "parametric_pdf_"+bin.name
            w = ROOT.RooWorkspace(wsName,wsName)
            for sample,config in bin.parameterDict.iteritems():
                if (sample not in bkg_names and sample not in data_names) and sample not in signal_model.signal_list: continue
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

        if option.epsilon:
            bin.parameterList = [epsilon_name,]
            bin.paramDict = {
                    epsilon_name: [epsilon_name,"0.02","0.002.","[-5,5]"],
                    }
        #dataCard.makeCard(cardDir,binListCopy)
        #dataCard.makeCard(cardDir,[bin],appendToPath=bin.name)
        dataCard.makeCard(cardDir,[bin],appendToPath=option.appendToPath if option.appendToPath else "")
        reader.end()
