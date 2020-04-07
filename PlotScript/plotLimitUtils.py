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

def makeLimitDict(inputDir,selectStr,method,massCut):
    outDict = OrderedDict()
    for quantile in quantiles:
        outDict[quantile.name] = OrderedDict()
    for cardDir in glob.glob(inputDir+"*"+selectStr+"*/"):
        print "Reading directory "+cardDir
        window_name = cardDir.split("/")[-2]
        window_value = float(window_name.split("_")[1].replace("MZD",""))
        if window_value > massCut: continue
        for i,quan in enumerate(quantiles):
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
    return outDict
