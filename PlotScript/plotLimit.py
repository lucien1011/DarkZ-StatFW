import ROOT,glob,os,argparse,subprocess,array,math
from collections import OrderedDict
import Utils.CMS_lumi as CMS_lumi
import Utils.tdrstyle as tdrstyle

from Physics.Zd_XS import *

ROOT.gROOT.SetBatch(ROOT.kTRUE)

parser = argparse.ArgumentParser()
parser.add_argument("--inputDir",action="store")
parser.add_argument("--outputPath",action="store")
parser.add_argument("--selectStr",action="store",default="")

option = parser.parse_args()

inputDir = option.inputDir

# ________________________________________________________________ ||
# CMS style
# ________________________________________________________________ ||
CMS_lumi.cmsText = "CMS"
CMS_lumi.extraText = "Preliminary"
CMS_lumi.cmsTextSize = 0.65
CMS_lumi.outOfFrame = True
#CMS_lumi.lumi_13TeV = "77.3 fb^{-1}"
#CMS_lumi.lumi_13TeV = "35.9 fb^{-1}"
CMS_lumi.lumi_13TeV = "136.1 fb^{-1}"
#CMS_lumi.lumi_13TeV = "150 fb^{-1}"
tdrstyle.setTDRStyle()

setLogY         = False
expOnly         = True 
#quantiles       = ["down2","down1","central","up1","up2","obs"]
quantiles       = ["down2","down1","central","up1","up2",]
varName         = "limit"
#plots           = ["epsilon","BrHZZd"]
#plots           = ["kappa","BrHZdZd"]
plots           = ["epsilon_EpsPOI"]
#plots           = ["BrHZZd"]
maxFactor       = 1.5
y_label_dict    = {
                    "epsilon": "#varepsilon",
                    "epsilon_EpsPOI": "#varepsilon",
                    "kappa": "#kappa",
                    "BrHZZd": "Br(h #rightarrow Z Z_{d})",
                    "BrHZdZd": "Br(h #rightarrow Z_{d} Z_{d})",
                  }

def calculate(r_value,window_value,what):
    if what == "epsilon":
        return epsilon*math.sqrt(r_value)
    elif what == "kappa":
        return kappa*math.sqrt(r_value)
    elif what == "BrHZdZd":
        return r_value*xs_HZdZd_dict[window_value]/xs_brHZdZd_dict[window_value]
    elif what == "BrHZZd":
        return r_value*xs_dict[window_value]/xs_brHZZd_dict[window_value]
    elif what == "epsilon_EpsPOI":
        return r_value
    else:
        raise RuntimeError

# ________________________________________________________________ ||
# Read limit from directory
# ________________________________________________________________ ||
outDict = OrderedDict()
for quantile in quantiles:
    outDict[quantile] = OrderedDict()
for cardDir in glob.glob(inputDir+"*"+option.selectStr+"*/"):
    print "Reading directory "+cardDir
    inputFile = ROOT.TFile(cardDir+"higgsCombineTest.AsymptoticLimits.mH120.root","READ")
    tree = inputFile.Get("limit")
    window_name = cardDir.split("/")[-2]
    #window_value = int(window_name.split("_")[1])
    #window_value = int(window_name.split("_")[1].replace("M",""))
    window_value = int(window_name.split("_")[1].replace("MZD",""))
    if expOnly:
        for i,entry in enumerate(tree):
            outDict[quantiles[i]][window_value] = getattr(entry,varName)
    else:
        raise RuntimeError

# ________________________________________________________________ ||
# Draw limit with outDict
# ________________________________________________________________ ||
outputDir = os.path.dirname(option.outputPath)
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
    frame.GetXaxis().SetTitle("m_{Z_{d}}")
    frame.SetMinimum(0)
    yellow = ROOT.TGraph(2*nPoints)
    green = ROOT.TGraph(2*nPoints)
    median = ROOT.TGraph(nPoints)
    CMS_lumi.CMS_lumi(c,4,11)
    window_values = outDict["central"].keys()
    window_values.sort()
    frame.GetXaxis().SetLimits(min(window_values),max(window_values))
    frame.SetMaximum(max([calculate(outDict[quan][window_value],window_value,plot) for quan in quantiles for window_value in window_values ])*maxFactor)
    for i,window_value in enumerate(window_values):
        yellow.SetPoint( i, window_value,   calculate(outDict["up2"][window_value]         , window_value, plot) )
        yellow.SetPoint( 2*nPoints-1-i, window_value,   calculate(outDict["down2"][window_value]       , window_value, plot) )
        green.SetPoint( i, window_value,    calculate(outDict["up1"][window_value]         , window_value, plot) )
        green.SetPoint( 2*nPoints-1-i, window_value,    calculate(outDict["down1"][window_value]       , window_value, plot) )
        median.SetPoint( i, window_value,   calculate(outDict["central"][window_value]     , window_value, plot) )
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
    
    if setLogY:
        c.SetLogy()

    c.SaveAs(option.outputPath.replace(".pdf","_"+plot+".pdf"))
