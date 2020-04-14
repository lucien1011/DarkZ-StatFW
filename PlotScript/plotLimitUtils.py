from Physics.ALP_XS import *
from Physics.Zd_XS import * 
from PlotScript.limitUtils import y_label_dict,calculate

import ROOT,glob,os,subprocess,array,math
from collections import OrderedDict
import CMS_lumi 
import tdrstyle 

from StatFW.BaseObject import BaseObject

ROOT.gROOT.SetBatch(ROOT.kTRUE)

# ________________________________________________________________ ||
# CMS style
# ________________________________________________________________ ||
CMS_lumi.cmsText = "CMS"
CMS_lumi.extraText = ""
ROOT.TGaxis.SetMaxDigits(8)
CMS_lumi.cmsTextSize = 0.65
CMS_lumi.outOfFrame = True
CMS_lumi.lumi_13TeV = "137 fb^{-1}"
tdrstyle.setTDRStyle()

quantiles       = [
    BaseObject("down2",
        asymp_file_name="higgsCombineTest.AsymptoticLimits.mH120.root",
        hybridnew_file_name="higgsCombineTest.HybridNew.mH120.quant0.025.root",
        ),
    BaseObject("down1",
        asymp_file_name="higgsCombineTest.AsymptoticLimits.mH120.root",
        hybridnew_file_name="higgsCombineTest.HybridNew.mH120.quant0.160.root",
        ),
    BaseObject("central",
        asymp_file_name="higgsCombineTest.AsymptoticLimits.mH120.root",
        hybridnew_file_name="higgsCombineTest.HybridNew.mH120.quant0.500.root",
        ),
    BaseObject("up1",
        asymp_file_name="higgsCombineTest.AsymptoticLimits.mH120.root",
        hybridnew_file_name="higgsCombineTest.HybridNew.mH120.quant0.840.root",
        ),
    BaseObject("up2",
        asymp_file_name="higgsCombineTest.AsymptoticLimits.mH120.root",
        hybridnew_file_name="higgsCombineTest.HybridNew.mH120.quant0.975.root",
        ),
    BaseObject("obs",
        asymp_file_name="higgsCombineTest.AsymptoticLimits.mH120.root",
        hybridnew_file_name="higgsCombineTest.HybridNew.mH120.root",
        ),
    ]
varName         = "limit"
lowBoxCut       = 8.0
highBoxCut      = 11.5

def makeLimitDict(inputDir,selectStr,method,massCutFunc,smoothing=False):
    outDict = OrderedDict()
    for quantile in quantiles:
        outDict[quantile.name] = OrderedDict()
    for cardDir in glob.glob(inputDir+"*"+selectStr+"*/"):
        print "Reading directory "+cardDir
        window_name = cardDir.split("/")[-2]
        window_value = float(window_name.split("_")[1].replace("MZD",""))
        if not massCutFunc(window_value): continue
        for i,quan in enumerate(quantiles):
            #try:
            if method == "AsymptoticLimits":
                inputFile = ROOT.TFile(cardDir+quan.asymp_file_name,"READ")
                tree = inputFile.Get("limit")
                tree.GetEntry(i)
                outDict[quan.name][window_value] = getattr(tree,varName)
                inputFile.Close()
            elif method == "HybridNew":
                inputFile = ROOT.TFile(cardDir+quan.hybridnew_file_name,"READ")
                tree = inputFile.Get("limit")
                tree.GetEntry(0)
                outDict[quan.name][window_value] = getattr(tree,varName)
                inputFile.Close()
            #except AttributeError:
            #    continue

    if smoothing:
        nPoints = len(outDict["central"])
        window_values = outDict["central"].keys()
        yellow_up = ROOT.TGraph(nPoints)
        yellow_down = ROOT.TGraph(nPoints)
        green_up = ROOT.TGraph(nPoints)
        green_down = ROOT.TGraph(nPoints)
        for i,window_value in enumerate(window_values):
            yellow_up.SetPoint(i,window_value,outDict["up2"][window_value]) 
            yellow_down.SetPoint(i,window_value,outDict["down2"][window_value]) 
            green_up.SetPoint(i,window_value,outDict["up1"][window_value]) 
            green_down.SetPoint(i,window_value,outDict["down1"][window_value])
        yellow_up_smooth = ROOT.TGraphSmooth()
        yellow_up = yellow_up_smooth.SmoothKern(yellow_up)
        yellow_down_smooth = ROOT.TGraphSmooth()
        yellow_down = yellow_down_smooth.SmoothSuper(yellow_down)
        green_up_smooth = ROOT.TGraphSmooth()
        green_up = green_up_smooth.SmoothKern(green_up)
        green_down_smooth = ROOT.TGraphSmooth()
        green_down = green_down_smooth.SmoothSuper(green_down)
        for q in ["up2","down2","up1","down1"]:
            outDict[q+"_smooth"] = {}
        for i,window_value in enumerate(window_values):
            outDict["up2_smooth"][window_value] = yellow_up.Eval(window_value)
            outDict["up1_smooth"][window_value] = green_up.Eval(window_value)
            outDict["down2_smooth"][window_value] = yellow_down.Eval(window_value)
            outDict["down1_smooth"][window_value] = green_down.Eval(window_value)

    return outDict
