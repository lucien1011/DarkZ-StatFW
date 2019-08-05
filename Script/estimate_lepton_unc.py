import ROOT,os
from StatFW.BaseObject import BaseObject

# ____________________________________________________________________________________ ||
#inputDir        = "/raid/raid7/lucien/Higgs/DarkZ/ParaInput/DarkPhotonSelection_m4l100To170_Nominal/2019-07-31_m4lSR-m4lSB_HZZd-ppZZd_Run2016/"
inputDir        = "/raid/raid7/lucien/Higgs/DarkZ/ParaInput/DarkPhotonSelection_m4l100To170_Nominal/2019-07-31_m4lSR-m4lSB_HZZd-ppZZd_Run2017/"
#inputDir        = "/raid/raid7/lucien/Higgs/DarkZ/ParaInput/DarkPhotonSelection_m4l100To170_Nominal/2019-07-31_m4lSR-m4lSB_HZZd-ppZZd_Run2018/"
massPoints      = [
                    7,
                    15,
                    30,
                    ]
sigModelStr     = "HZZd_M"
TFileName       = "StatInput.root"
finalStates     = [
                    BaseObject("MuMu_HiggsSR",width=0.02,lep_e_unc=0.2),
                    BaseObject("ElMu_HiggsSR",width=0.02,lep_e_unc=0.2),
                    BaseObject("ElEl_HiggsSR",width=0.05,lep_e_unc=0.2),
                    BaseObject("MuEl_HiggsSR",width=0.05,lep_e_unc=0.2),
                    ]

# ____________________________________________________________________________________ ||
for m in massPoints:
    print "="*20
    print "Mass point: "+sigModelStr+str(m)
    inputFilePath = os.path.join(inputDir,sigModelStr+str(m),TFileName)
    inputFile = ROOT.TFile(inputFilePath,"READ")
    for fs in finalStates:
        hist = inputFile.Get(fs.name)
        dnBin = hist.GetXaxis().FindBin(m*(1.-fs.width))
        upBin = hist.GetXaxis().FindBin(m*(1.+fs.width))
        dnBin_e_unc = hist.GetXaxis().FindBin(m*(1.-fs.width*(1.+fs.lep_e_unc)))
        upBin_e_unc = hist.GetXaxis().FindBin(m*(1.+fs.width*(1.+fs.lep_e_unc)))
        print fs.name+": "+str(hist.Integral(dnBin_e_unc,upBin_e_unc)/hist.Integral(dnBin,upBin))
    inputFile.Close()
