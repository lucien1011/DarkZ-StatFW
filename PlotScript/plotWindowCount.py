import os,copy,math,argparse,ROOT,bisect

from Utilities.Hist import getCountAndError,getIntegral
from Utilities.DataCard import SignalModel
from Utilities.mkdir_p import mkdir_p

from StatFW.BaseObject import BaseObject
from StatFW.FileReader import *

import Utilities.CMS_lumi as CMS_lumi
import Utilities.tdrstyle as tdrstyle

ROOT.gROOT.SetBatch(ROOT.kTRUE)
tdrstyle.setTDRStyle()
ROOT.gStyle.SetLabelSize(0.018,"XYZ")
ROOT.gStyle.SetLabelOffset(0.003, "XYZ")
ROOT.gStyle.SetTitleSize(0.035,"XYZ")
ROOT.gStyle.SetTitleXOffset(1.8)

# ____________________________________________________________________________________________________________________________________________ ||
#inputDir        = "/raid/raid7/lucien/Higgs/DarkZ/ParaInput/DarkPhotonSelection_m4l100To170_Nominal/2019-09-02_m4lSR-m4lSB_HZZd-ppZZd_RunII/"
#zxShapeDir      = "/raid/raid7/lucien/Higgs/DarkZ/ParaInput/DarkPhotonSelection_m4l100To170_Nominal/2019-09-02_m4lSR-m4lSB_HZZd-ppZZd_RunII/"
#outputDir       = "/home/lucien/public_html/Higgs/DarkZ/WindowCount/RunII/2019-08-19/"
#outputDir       = "/home/lucien/public_html/Higgs/DarkZ/WindowCount/RunII/2019-08-23/"
#outputDir       = "/home/lucien/public_html/Higgs/DarkZ/WindowCount/RunII/2019-09-02/"
#outputDir       = "/home/lucien/public_html/Higgs/DarkZ/WindowCount/RunII/2019-09-02/"
#mass_points     = [4.04*1.005**i for i in range(434)]

#inputDir        = "/raid/raid7/lucien/Higgs/HToZdZd/DarkPhotonSR/StatInput/2019-08-21_RunII/"
#zxShapeDir      = "/raid/raid7/lucien/Higgs/HToZdZd/DarkPhotonSR/StatInput/2019-08-21_RunII/"
inputDir        = "/raid/raid7/lucien/Higgs/HToZdZd/DarkPhotonSR/StatInput/2019-09-06_RunII/"
zxShapeDir      = "/raid/raid7/lucien/Higgs/HToZdZd/DarkPhotonSR/StatInput/2019-09-06_RunII/"
##outputDir       = "/home/lucien/public_html/Higgs/HToZdZd/WindowCount/RunII/2019-08-21/"
##outputDir       = "/home/lucien/public_html/Higgs/HToZdZd/WindowCount/RunII/2019-08-23/"
#outputDir       = "/home/lucien/public_html/Higgs/HToZdZd/WindowCount/RunII/2019-09-02/"
outputDir       = "/home/lucien/public_html/Higgs/HToZdZd/WindowCount/RunII/2019-09-06/"
mass_points     = [4.04*1.005**i for i in range(551)]

TFileName       = "StatInput.root"

channels        = [
                    #BaseObject("MuMu_HiggsSR",inputBinName="MuMu_HiggsSR",width=0.02),
                    #BaseObject("ElMu_HiggsSR",inputBinName="ElMu_HiggsSR",width=0.02),
                    #BaseObject("ElEl_HiggsSR",inputBinName="ElEl_HiggsSR",width=0.05),
                    #BaseObject("MuEl_HiggsSR",inputBinName="MuEl_HiggsSR",width=0.05),
                    #BaseObject("MuMu_HiggsLowSB",inputBinName="MuMu_HiggsLowSB",width=0.02),
                    #BaseObject("ElMu_HiggsLowSB",inputBinName="ElMu_HiggsLowSB",width=0.02),
                    #BaseObject("ElEl_HiggsLowSB",inputBinName="ElEl_HiggsLowSB",width=0.05),
                    #BaseObject("MuEl_HiggsLowSB",inputBinName="MuEl_HiggsLowSB",width=0.05),
                    #BaseObject("MuMu_HiggsHighSB",inputBinName="MuMu_HiggsHighSB",width=0.02),
                    #BaseObject("ElMu_HiggsHighSB",inputBinName="ElMu_HiggsHighSB",width=0.02),
                    #BaseObject("ElEl_HiggsHighSB",inputBinName="ElEl_HiggsHighSB",width=0.05),
                    #BaseObject("MuEl_HiggsHighSB",inputBinName="MuEl_HiggsHighSB",width=0.05),
                    
                    BaseObject("Mu",inputBinName="Mu",width=0.02),
                    BaseObject("El",inputBinName="El",width=0.05),
                ]
bkgs            = [
                   BaseObject("qqZZ",color=ROOT.kBlue+2,latexName="qqZZ",),
                   BaseObject("Higgs",color=ROOT.kAzure-2,latexName="Higgs",),
                   BaseObject("ggZZ",color=ROOT.kBlue,latexName="ggZZ",),
                   BaseObject("ZPlusX",
                       inputDir=zxShapeDir,
                       TFileName="ParaShape.root",
                       color=ROOT.kGreen,
                       latexName="Z+X",
                       ),
                ]
sigs            = [
                    #BaseObject("HZZd_M4",color=ROOT.kRed,latexName="h #rightarrow ZZ_{d}, m_{Z_{d}} = 4 GeV",),
                    #BaseObject("HZZd_M7",color=ROOT.kRed+1,latexName="h #rightarrow ZZ_{d}, m_{Z_{d}} = 7 GeV",),
                    #BaseObject("HZZd_M10",color=ROOT.kRed-2,latexName="h #rightarrow ZZ_{d}, m_{Z_{d}} = 10 GeV",),
                    #BaseObject("HZZd_M15",color=ROOT.kRed+2,latexName="h #rightarrow ZZ_{d}, m_{Z_{d}} = 15 GeV",),
                    #BaseObject("HZZd_M25",color=ROOT.kRed-2,latexName="h #rightarrow ZZ_{d}, m_{Z_{d}} = 25 GeV",),
                    #BaseObject("HZZd_M30",color=ROOT.kRed+3,latexName="h #rightarrow ZZ_{d}, m_{Z_{d}} = 30 GeV",),
                    #BaseObject("ppZZd4l_M5",color=ROOT.kGreen,latexName="pp #rightarrow ZZ_{d}, m_{Z_{d}} = 5 GeV",),
                    #BaseObject("ppZZd4l_M15",color=ROOT.kGreen+1,latexName="pp #rightarrow ZZ_{d}, m_{Z_{d}} = 15 GeV",),
                    #BaseObject("ppZZd4l_M30",color=ROOT.kGreen-1,latexName="pp #rightarrow ZZ_{d}, m_{Z_{d}} = 30 GeV",),
                    
                    BaseObject("HToZdZd_MZD4",color=ROOT.kRed,latexName="H #rightarrow Z_{d}Z_{d}, m_{Z_{d}} = 4 GeV",),
                    BaseObject("HToZdZd_MZD10",color=ROOT.kRed-1,latexName="H #rightarrow Z_{d}Z_{d}, m_{Z_{d}} = 10 GeV",),
                    BaseObject("HToZdZd_MZD20",color=ROOT.kRed+1,latexName="H #rightarrow Z_{d}Z_{d}, m_{Z_{d}} = 20 GeV",),
                    BaseObject("HToZdZd_MZD30",color=ROOT.kRed-2,latexName="H #rightarrow Z_{d}Z_{d}, m_{Z_{d}} = 30 GeV",),
                    BaseObject("HToZdZd_MZD40",color=ROOT.kRed+2,latexName="H #rightarrow Z_{d}Z_{d}, m_{Z_{d}} = 40 GeV",),
                    BaseObject("HToZdZd_MZD50",color=ROOT.kRed-3,latexName="H #rightarrow Z_{d}Z_{d}, m_{Z_{d}} = 50 GeV",),
                    BaseObject("HToZdZd_MZD60",color=ROOT.kRed+3,latexName="H #rightarrow Z_{d}Z_{d}, m_{Z_{d}} = 60 GeV",),
                ]

data            = BaseObject("Data",)

CMS_lumi.cmsText        = "CMS Preliminary"
CMS_lumi.extraText      = ""
CMS_lumi.cmsTextSize    = 0.65
CMS_lumi.outOfFrame     = True
#CMS_lumi.lumi_13TeV    = "77.3 fb^{-1}"
#CMS_lumi.lumi_13TeV    = "35.9 fb^{-1}"
CMS_lumi.lumi_13TeV     = "136.1 fb^{-1}"
#CMS_lumi.lumi_13TeV    = "150 fb^{-1}"
maxFactor               = 4.0
drawVetoBox             = True
vetoMassRange           = [8.5,11.0]

# ____________________________________________________________________________________________________________________________________________ ||
print("Mass range: "+str(mass_points[0])+"-"+str(mass_points[-1]))

# ____________________________________________________________________________________________________________________________________________ ||
mkdir_p(outputDir)
for channel in channels: channel.histDict = {}
reader = FileReader()
for channel in channels:
    c = ROOT.TCanvas()
    #c = ROOT.TCanvas("c_"+channel.name,"",0,0,100,100)
    channel.histDict = {}
    channel.tstack = ROOT.THStack("stackHist_"+channel.name,";Window index (mass);Event yield/window width")
    for sample in bkgs+sigs+[data,]: 
        channel.histDict[sample.name] = ROOT.TH1D("_".join(["hist",channel.name,sample.name]),"",len(mass_points),-0.5,len(mass_points))
    for ibin,m in enumerate(mass_points):
        window_width = 2*channel.width*m
        for sample in bkgs+sigs+[data,]:
            sampleName = sample.name
            reader.openFile(inputDir if not hasattr(sample,"inputDir") else sample.inputDir,sampleName,TFileName if not hasattr(sample,"TFileName") else sample.TFileName)
            hist = reader.getObj(sampleName,channel.inputBinName)
            count,error = getCountAndError(hist,m,channel.width,isSR=True)
            channel.histDict[sample.name].SetBinContent(ibin+1,count/window_width)
            channel.histDict[sample.name].SetBinError(ibin+1,error/window_width)
            channel.histDict[sample.name].GetXaxis().SetBinLabel(ibin+1,str(ibin+1)+" (%4.4f)"%m if ibin % 20 == 0 else "")
    channel.errHist = ROOT.TH1D("_".join(["errHist",channel.name,]),"",len(mass_points),-0.5,len(mass_points))
    nbins = channel.errHist.GetNbinsX()
    for bkg in reversed(bkgs):
        for ibin in range(nbins):
            channel.errHist.SetBinContent(ibin+1,channel.errHist.GetBinContent(ibin+1)+channel.histDict[bkg.name].GetBinContent(ibin+1))
            channel.errHist.SetBinError(ibin+1,channel.errHist.GetBinError(ibin+1)+channel.histDict[bkg.name].GetBinError(ibin+1)**2)
            channel.histDict[bkg.name].SetBinError(ibin+1,0.)
        channel.histDict[bkg.name].SetFillColor(bkg.color)
        channel.histDict[bkg.name].SetLineWidth(1)
        channel.histDict[bkg.name].GetYaxis().SetTitle("Event yield/window width")
        channel.histDict[bkg.name].GetXaxis().SetTitle("Window index")
        channel.tstack.Add(channel.histDict[bkg.name])
    for ibin in range(nbins):
        channel.errHist.SetBinError(ibin+1,math.sqrt(channel.errHist.GetBinError(ibin+1)))
    maximum = max([channel.errHist.GetMaximum()]+[channel.histDict[sig.name].GetMaximum() for sig in sigs])
    channel.tstack.SetMaximum(maxFactor*maximum)
    channel.tstack.Draw()
    for sig in sigs:
        channel.histDict[sig.name].SetLineColor(sig.color)
        channel.histDict[sig.name].SetLineStyle(9)
        channel.histDict[sig.name].Draw("histsame")
    channel.errHist.SetMarkerStyle(1)
    channel.errHist.SetLineWidth(1)
    channel.errHist.SetLineColor(1)
    channel.errHist.SetFillColor(1)
    channel.errHist.SetFillStyle(3004)
    channel.errHist.Draw("samee2")
    channel.histDict[data.name].SetLineWidth(1)
    channel.histDict[data.name].SetLineColor(1)
    channel.histDict[data.name].SetMarkerStyle(6)
    channel.histDict[data.name].SetMarkerSize(0.0001)
    channel.histDict[data.name].Draw("samep")
    leg = ROOT.TLegend(0.70,0.70,0.89,0.92)
    leg.SetBorderSize(0)
    leg.SetFillColor(0)
    leg.SetTextSize(0.015)
    for bkg in reversed(bkgs): leg.AddEntry(channel.histDict[bkg.name],bkg.latexName,"f")
    for sig in reversed(sigs): leg.AddEntry(channel.histDict[sig.name],sig.latexName,"l")
    leg.Draw("same")
    CMS_lumi.CMS_lumi(c,4,11)
    if drawVetoBox:
        box = ROOT.TBox(bisect.bisect(mass_points,vetoMassRange[0]),0.,bisect.bisect(mass_points,vetoMassRange[1]),maxFactor*maximum)
        box.SetFillColor(ROOT.kGray)
        box.Draw('same')
    c.SaveAs(os.path.join(outputDir,channel.name+".pdf"))
    reader.end()
