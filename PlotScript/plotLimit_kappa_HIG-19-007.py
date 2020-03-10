import ROOT,glob,os,subprocess,array,math
from collections import OrderedDict
import CMS_lumi 
import tdrstyle 

from Physics.ALP_XS import *
from PlotScript.limitUtils import y_label_dict,calculate

ROOT.gROOT.SetBatch(ROOT.kTRUE)

#inputDir = "/home/lucien/AnalysisCode/Higgs/DarkZ-StatFW-2/HToZdZd_DataCard/2019-12-17_SR2D_RunII/"
#outputPath = "/home/lucien/public_html/Higgs/HToZdZd/Limit/2020-02-26_SR2D_RunII/ExpObsLimit.pdf" 
#selectStr = ""

#inputDir = "/home/lucien/AnalysisCode/Higgs/DarkZ-StatFW/HToZdZd_DataCard/2020-03-03_SR2D_RunII/"
#outputPath = "/home/lucien/public_html/Higgs/HToZdZd/Limit/2020-03-03_SR2D_RunII/ExpObsLimit.pdf" 
#selectStr = ""

inputDir = "/home/lucien/AnalysisCode/Higgs/DarkZ-StatFW/HToZdZd_DataCard/2020-03-06_SR2D_RunII/"
outputPath = "/home/lucien/public_html/Higgs/HToZdZd/Limit/2020-03-06_SR2D_RunII/ExpObsLimit.pdf" 
selectStr = ""

# ________________________________________________________________ ||
# CMS style
# ________________________________________________________________ ||
CMS_lumi.cmsText = "CMS"
CMS_lumi.extraText = ""
ROOT.TGaxis.SetMaxDigits(8)
CMS_lumi.cmsTextSize = 0.65
CMS_lumi.outOfFrame = True
CMS_lumi.lumi_13TeV = "136.1 fb^{-1}"
tdrstyle.setTDRStyle()

setLogY         = True
#expOnly         = True 
quantiles       = ["down2","down1","central","up1","up2","obs"]
varName         = "limit"
plots           = ["kappa"]
#maxFactor       = 1E3
y_min           = 1E-6
maxFactor       = 100
x_label         = "m_{Z_{d}}"
drawVetoBox     = True

# ________________________________________________________________ ||
# Read limit from directory
# ________________________________________________________________ ||
outDict = OrderedDict()
for quantile in quantiles:
    outDict[quantile] = OrderedDict()
for cardDir in glob.glob(inputDir+"*"+selectStr+"*/"):
    print "Reading directory "+cardDir
    inputFile = ROOT.TFile(cardDir+"higgsCombineTest.AsymptoticLimits.mH120.root","READ")
    tree = inputFile.Get("limit")
    window_name = cardDir.split("/")[-2]
    #window_value = int(window_name.split("_")[1])
    #window_value = int(window_name.split("_")[1].replace("M",""))
    window_value = float(window_name.split("_")[1].replace("MZD",""))
    if window_value > higgs_boson.mass/2.: continue
    for i,entry in enumerate(tree):
        outDict[quantiles[i]][window_value] = getattr(entry,varName)
    #if expOnly:
    #    for i,entry in enumerate(tree):
    #        outDict[quantiles[i]][window_value] = getattr(entry,varName)
    #else:
    #    raise RuntimeError

# ________________________________________________________________ ||
# Draw limit with outDict
# ________________________________________________________________ ||
outputDir = os.path.dirname(outputPath)
if not os.path.exists(outputDir):
    os.makedirs(outputDir)
nPoints = len(outDict["central"])
outGraphDict = {}
for plot in plots:
    W = 800
    H  = 600
    T = 0.08*H
    B = 0.12*H
    L = 0.12*W
    R = 0.04*W
    c = ROOT.TCanvas("c","c",100,100,W,H)
    c.SetFillColor(0)
    c.SetBorderMode(0)
    c.SetFrameFillStyle(0)
    c.SetFrameBorderMode(0)
    c.SetLeftMargin( L/W )
    c.SetRightMargin( R/W )
    c.SetTopMargin( T/H )
    c.SetBottomMargin( B/H )
    c.SetTickx(0)
    c.SetTicky(0)
    c.SetGrid()
    c.cd()
    frame = c.DrawFrame(1.4,0.001, 4.1, 10)
    frame.GetYaxis().CenterTitle()
    frame.GetYaxis().SetTitleSize(0.05)
    frame.GetXaxis().SetTitleSize(0.05)
    frame.GetXaxis().SetLabelSize(0.04)
    frame.GetYaxis().SetLabelSize(0.03)
    frame.GetYaxis().SetTitleOffset(1.2)
    frame.GetXaxis().SetNdivisions(508)
    frame.GetYaxis().CenterTitle(True)
    #frame.GetYaxis().SetTitle("95% upper limit on #sigma / #sigma_{SM}")
    frame.GetYaxis().SetTitle(y_label_dict[plot])
    frame.GetXaxis().SetTitle(x_label)
    frame.SetMinimum(0)
    yellow = ROOT.TGraph(2*nPoints)
    green = ROOT.TGraph(2*nPoints)
    median = ROOT.TGraph(nPoints)
    black = ROOT.TGraph(nPoints)
    CMS_lumi.CMS_lumi(c,4,0)
    window_values = outDict["central"].keys()
    window_values.sort()
    frame.GetXaxis().SetLimits(min(window_values),max(window_values))
    frameMax = max([calculate(outDict[quan][window_value],window_value,plot) for quan in quantiles for window_value in window_values ])*maxFactor
    frame.SetMaximum(frameMax)
    if setLogY: frame.SetMinimum(y_min)
    for i,window_value in enumerate(window_values):
        yellow.SetPoint( i, window_value,calculate(outDict["up2"][window_value], window_value, plot) )
        yellow.SetPoint( 2*nPoints-1-i, window_value,calculate(outDict["down2"][window_value], window_value, plot) )
        green.SetPoint( i, window_value,calculate(outDict["up1"][window_value], window_value, plot) )
        green.SetPoint( 2*nPoints-1-i, window_value,calculate(outDict["down1"][window_value], window_value, plot) )
        median.SetPoint( i, window_value,calculate(outDict["central"][window_value], window_value, plot) )
        black.SetPoint( i, window_value,calculate(outDict["obs"][window_value], window_value, plot) )
    yellow.SetFillColor(ROOT.kOrange)
    yellow.SetLineColor(ROOT.kOrange)
    yellow.SetFillStyle(1001)
    yellow.Draw('F')

    green.SetFillColor(ROOT.kGreen+1)
    green.SetLineColor(ROOT.kGreen+1)
    green.SetFillStyle(1001)
    green.Draw('Fsame')

    median.SetLineColor(1)
    median.SetLineWidth(2)
    median.SetLineStyle(2)
    median.Draw('Lsame')

    black.SetLineColor(1)
    black.SetLineWidth(2)
    black.SetLineStyle(1)
    black.Draw('Lsame')
    
    if setLogY:
        c.SetLogy()

    if drawVetoBox:
        box = ROOT.TBox(8.5,0.,11.,frameMax)
        box.SetFillColor(ROOT.kGray)
        box.Draw('same')

    c.SaveAs(outputPath.replace(".pdf","_"+plot+".pdf"))
