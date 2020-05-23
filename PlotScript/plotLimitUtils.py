from Physics.ALP_XS import *
from Physics.Zd_XS import * 
from PlotScript.limitUtils import y_label_dict,calculate

import ROOT,glob,os,subprocess,array,math,pickle
from collections import OrderedDict
import CMS_lumi 
import tdrstyle 

from StatFW.BaseObject import BaseObject

ROOT.gROOT.SetBatch(ROOT.kTRUE)

# ________________________________________________________________ ||
# CMS style
# ________________________________________________________________ ||
CMS_lumi.cmsText = "CMS"
CMS_lumi.extraText = "Preliminary"
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

def makeLimitDict(inputDir,selectStr,method,massCutFunc,smoothing=False,dcDir=None,smooth_ranges=[]):
    outDict = OrderedDict()
    for quantile in quantiles:
        outDict[quantile.name] = OrderedDict()
    for cardDir in glob.glob(inputDir+"*"+selectStr+"*/"):
        if not os.path.isdir(cardDir): continue
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

    if dcDir:
        window_values = outDict["central"].keys()
        dc_dict = {}
        for i,window_value in enumerate(window_values):
            name = "Zd_MZD"+str(window_value)
            dcPath = os.path.join(dcDir,name,name+".txt")
            lines = open(dcPath,"r").readlines()
            for l in lines:
                if l.startswith("observation"):
                    dc_dict[window_value] = sum([int(n) for n in l.split()[1:]])
        window_values_with_data = [w for w,dcount in dc_dict.iteritems() if dcount > 0]
        print("window_values_with_data: ",window_values_with_data)

    if smoothing:
        nPoints = len(outDict["central"])
        window_values = outDict["central"].keys()
        yellow_up = ROOT.TGraph(nPoints)
        yellow_down = ROOT.TGraph(nPoints)
        green_up = ROOT.TGraph(nPoints)
        green_down = ROOT.TGraph(nPoints)
        median = ROOT.TGraph(nPoints)
        observe = ROOT.TGraph(nPoints)
        for i,window_value in enumerate(window_values):
            yellow_up.SetPoint(i,window_value,outDict["up2"][window_value]) 
            yellow_down.SetPoint(i,window_value,outDict["down2"][window_value]) 
            green_up.SetPoint(i,window_value,outDict["up1"][window_value]) 
            green_down.SetPoint(i,window_value,outDict["down1"][window_value])
            median.SetPoint(i,window_value,outDict["central"][window_value])
            observe.SetPoint(i,window_value,outDict["obs"][window_value])
        yellow_up_smooth = ROOT.TGraphSmooth()
        #yellow_up = yellow_up_smooth.SmoothSuper(yellow_up,"",0.5)
        yellow_up = yellow_up_smooth.SmoothKern(yellow_up,"normal",2.0)
        yellow_down_smooth = ROOT.TGraphSmooth()
        #yellow_down = yellow_down_smooth.SmoothSuper(yellow_down,"",0.5)
        yellow_down = yellow_down_smooth.SmoothKern(yellow_down,"normal",2.0)
        green_up_smooth = ROOT.TGraphSmooth()
        #green_up = green_up_smooth.SmoothSuper(green_up,"",0.5)
        green_up = green_up_smooth.SmoothKern(green_up,"normal",2.0)
        green_down_smooth = ROOT.TGraphSmooth()
        #green_down = green_down_smooth.SmoothSuper(green_down,"",0.5)
        green_down = green_down_smooth.SmoothKern(green_down,"normal",2.0)
        median_smooth = ROOT.TGraphSmooth()
        median = median_smooth.SmoothKern(median,"normal",2.0)
        observe_smooth = ROOT.TGraphSmooth()
        observe = observe_smooth.SmoothKern(observe)    
        for q in ["up2","down2","up1","down1","obs","central"]:
            outDict[q+"_smooth"] = {}
        for i,window_value in enumerate(window_values):
            if dc_dict and (dc_dict[window_value] > 0 or any(smooth_range[0] < window_value and smooth_range[1] > smooth_range for smooth_range in smooth_ranges)):
                outDict["obs_smooth"][window_value] = outDict["obs"][window_value]
            else:
                outDict["obs_smooth"][window_value] = observe.Eval(window_value)
            #outDict["central_smooth"][window_value] = outDict["central"][window_value]
            #outDict["up2_smooth"][window_value] = outDict["up2"][window_value]
            #outDict["up1_smooth"][window_value] = outDict["up1"][window_value]
            #outDict["down2_smooth"][window_value] = outDict["down2"][window_value]
            #outDict["down1_smooth"][window_value] = outDict["down1"][window_value]
            outDict["central_smooth"][window_value] = median.Eval(window_value)
            outDict["up2_smooth"][window_value] = yellow_up.Eval(window_value)
            outDict["up1_smooth"][window_value] = green_up.Eval(window_value)
            outDict["down2_smooth"][window_value] = yellow_down.Eval(window_value)
            outDict["down1_smooth"][window_value] = green_down.Eval(window_value)

    return outDict

def redrawBorder():
   ROOT.gPad.Update()
   ROOT.gPad.RedrawAxis()
   l = ROOT.TLine()
   l.DrawLine(ROOT.gPad.GetUxmin(), ROOT.gPad.GetUymax(), ROOT.gPad.GetUxmax(), ROOT.gPad.GetUymax())
   l.DrawLine(ROOT.gPad.GetUxmax(), ROOT.gPadGetUymin(), ROOT.gPad.GetUxmax(), ROOT.gPad.GetUymax())
