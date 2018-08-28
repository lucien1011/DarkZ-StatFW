import os,copy

from StatFW.DataCard import *
from StatFW.MassWindow import *
from StatFW.Systematic import *
from StatFW.Process import *
from StatFW.Reader import *
from StatFW.Channel import Bin

from Core.Collector import Collector

from Dataset.ComponentList import componentList
from Dataset.MergeSampleDict import mergeSampleDict

from Core.OutputInfo import OutputInfo

import math,argparse

# ____________________________________________________________________________________________________________________________________________ ||
parser = argparse.ArgumentParser()
parser.add_argument("--inputDir",action="store")
parser.add_argument("--verbose",action="store_true")

option = parser.parse_args()

# ____________________________________________________________________________________________________________________________________________ ||
# Configurable
inputDir = option.inputDir
commonLnSystFilePath = "/home/lucien/Higgs/DarkZ/DarkZ-StatFW/Config/CommonSyst.txt"
lnSystFilePathDict = {
        "FourEl": "/home/lucien/Higgs/DarkZ/DarkZ-StatFW/Config/Syst_4e.txt", 
        "FourMu": "/home/lucien/Higgs/DarkZ/DarkZ-StatFW/Config/Syst_4mu.txt", 
        "TwoElTwoMu": "/home/lucien/Higgs/DarkZ/DarkZ-StatFW/Config/Syst_2e2mu.txt", 
        }
outputDir = "/home/lucien/Higgs/DarkZ/DarkZ-StatFW/DataCard/2018-08-24/"

outputInfo              = OutputInfo("OutputInfo")
outputInfo.outputDir    = inputDir
outputInfo.TFileName    = "StatInput.root"
setDataToMC             = True

# ____________________________________________________________________________________________________________________________________________ ||
# mass window
mass_window_list = [
        MassWindow(15,0.02),
        MassWindow(20,0.02),
        MassWindow(25,0.02),
        MassWindow(30,0.02),
        ]

# ____________________________________________________________________________________________________________________________________________ ||
# bin list
binList = [
        Bin("FourEl",sysFile=lnSystFilePathDict["FourEl"],inputBinName="4e",),
        Bin("FourMu",sysFile=lnSystFilePathDict["FourMu"],inputBinName="4mu",),
        Bin("TwoElTwoMu",sysFile=lnSystFilePathDict["TwoElTwoMu"],inputBinName="2e2mu"),
        ]

# ____________________________________________________________________________________________________________________________________________ ||
# syst
lnSystReader = LogNormalSystReader()
commonLnSystematics = lnSystReader.makeLnSyst(commonLnSystFilePath)

# ____________________________________________________________________________________________________________________________________________ ||
collector = Collector()
collector.makeSampleList(componentList)
collector.makeMergedSampleList(componentList,mergeSampleDict)
collector.openFiles(collector.samples+collector.mergeSamples,outputInfo)

if not os.path.exists(os.path.abspath(outputDir)):
    os.makedirs(os.path.abspath(outputDir))

for window in mass_window_list:
    if option.verbose: print "*"*100
    if option.verbose: print "Making data card for ",window.getBinName()
    binListCopy = copy.deepcopy(binList)
    for bin in binListCopy:
        if option.verbose: print "-"*20
        if option.verbose: print bin.name
        # Get background count
        #for bkgName in collector.bkgSamples:
        totalBkgCount = 0.
        for bkgName in collector.mergeSamples:
            #histName = "_".join([window.makeHistName(),bkgName,bin.name,])
            histName = "_".join([window.makeHistName(),bin.inputBinName,])
            hist = collector.getObj(bkgName,histName)
            count = hist.GetBinContent(1) if bkgName != "ZPlusX" else hist.GetBinContent(1)*77.30/35.9
            error = hist.GetBinError(1)
            process = Process(bkgName,count if count >= 0. else 0.,error)
            totalBkgCount += count if count >= 0. else 0.
            bin.processList.append(process)
        if option.verbose: print "Total bkg count: ", totalBkgCount
        # Get data count
        dataCount = 0.
        for sample in collector.dataSamples:
            #histName = "_".join([window.makeHistName(),sample,bin.name,])
            histName = "_".join([window.makeHistName(),bin.inputBinName,])
            hist = collector.getObj(sample,histName)
            count = hist.GetBinContent(1)
            dataCount += count
            error = hist.GetBinError(1)
        bin.data = Process("data_obs",int(dataCount) if not setDataToMC else int(totalBkgCount),math.sqrt(int(dataCount)))
        if option.verbose: print "Total data count: ", dataCount
        for sigSample in collector.signalSamples:
            if bin.isSignal(sigSample) and window.matchSample(sigSample): break
        #histName = "_".join([window.makeHistName(),sigSample,bin.name,])
        histName = "_".join([window.makeHistName(),bin.inputBinName,])
        sigHist = collector.getObj(sigSample,histName)
        bin.processList.append(Process(sigSample,sigHist.GetBinContent(1),sigHist.GetBinError(1)))
        if option.verbose: print "Total signal count: ", sigHist.GetBinContent(1)
        bin.systList = []
        for syst in commonLnSystematics:
            bin.systList.append(copy.deepcopy(syst))
        bin.systList += lnSystReader.makeLnSyst(bin.sysFile)
    dataCard = DataCard(window) 
    dataCard.makeCard(outputDir,binListCopy)

collector.closeFiles()
