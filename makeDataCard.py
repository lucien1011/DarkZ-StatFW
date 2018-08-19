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

import math

# ____________________________________________________________________________________________________________________________________________ ||
# Configurable
inputDir = "/raid/raid7/lucien/Higgs/DarkZ/StatInput/test/2018-08-13/"
lnSystFilePath = "/home/lucien/UF-PyNTupleRunner/DarkZ/StatTools/Syst.txt"
outputDir = "/home/lucien/Higgs/DarkZ/DarkZ-StatFW/DataCard/2018-08-17/"

outputInfo              = OutputInfo("OutputInfo")
outputInfo.outputDir    = inputDir
outputInfo.TFileName    = "StatInput.root"

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
        Bin("FourEl",sysFile=lnSystFilePath,inputBinName="4e",),
        Bin("FourMu",sysFile=lnSystFilePath,inputBinName="4mu",),
        Bin("TwoElTwoMu",sysFile=lnSystFilePath,inputBinName="2e2mu"),
        ]

# ____________________________________________________________________________________________________________________________________________ ||
# syst
lnSystReader = LogNormalSystReader()
lnSystematics = lnSystReader.makeLnSyst(lnSystFilePath)

# ____________________________________________________________________________________________________________________________________________ ||
collector = Collector()
collector.makeSampleList(componentList)
collector.makeMergedSampleList(componentList,mergeSampleDict)
collector.openFiles(collector.samples+collector.mergeSamples,outputInfo)

if not os.path.exists(os.path.abspath(outputDir)):
    os.makedirs(os.path.abspath(outputDir))

for window in mass_window_list:
    for bin in binList:
        # Get background count
        #for bkgName in collector.bkgSamples:
        for bkgName in collector.mergeSamples:
            #histName = "_".join([window.makeHistName(),bkgName,bin.name,])
            histName = "_".join([window.makeHistName(),bin.inputBinName,])
            hist = collector.getObj(bkgName,histName)
            count = hist.GetBinContent(1)
            error = hist.GetBinError(1)
            process = Process(bkgName,count,error)
            bin.processList.append(process)
        # Get data count
        dataCount = 0.
        for sample in collector.dataSamples:
            #histName = "_".join([window.makeHistName(),sample,bin.name,])
            histName = "_".join([window.makeHistName(),bin.inputBinName,])
            hist = collector.getObj(sample,histName)
            count = hist.GetBinContent(1)
            dataCount += count
            error = hist.GetBinError(1)
        bin.data = Process("data_obs",int(dataCount),math.sqrt(int(dataCount)))
        for sigSample in collector.signalSamples:
            if bin.isSignal(sigSample) and window.matchSample: break
        #histName = "_".join([window.makeHistName(),sigSample,bin.name,])
        histName = "_".join([window.makeHistName(),bin.inputBinName,])
        sigHist = collector.getObj(sigSample,histName)
        bin.processList.append(Process(sigSample,sigHist.GetBinContent(1),sigHist.GetBinError(1)))
        bin.systList = []
        for syst in lnSystematics:
            bin.systList.append(copy.deepcopy(syst))
    dataCard = DataCard(window) 
    dataCard.makeCard(outputDir,binList)

collector.closeFiles()
