import ROOT,glob,os,argparse,subprocess,array,math
from collections import OrderedDict
import Utils.CMS_lumi as CMS_lumi
import Utils.tdrstyle as tdrstyle

from Physics.HZZd_XS import *

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
CMS_lumi.lumi_13TeV = "150 fb^{-1}"
tdrstyle.setTDRStyle()

expOnly         = True 
quantiles       = ["down2","down1","central","up1","up2","obs"]
varName         = "limit"
plots           = ["epsilon","BrHZZd"]
maxFactor       = 1.5
y_label_dict    = {
                    "epsilon": "#varepsilon",
                    "BrHZZd": "Br(h #rightarrow Z Z_{d})",
                  }

def calculate(r_value,window_value,what):
    if what == "epsilon":
        return epsilon*math.sqrt(r_value)
    elif what == "BrHZZd":
        return r_value*xs_dict[window_value]/xs_brHZZd_dict[window_value]
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
    window_value = int(window_name.split("_")[1])
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

    c.SaveAs(option.outputPath.replace(".pdf","_"+plot+".pdf"))
        
    #x_list = []
    #y_xs_list = []
    #y_epsilon_list = []
    #y_br4l_list = []
    #y_brHZZd_list = []
    #y_brHZX_XToll_list = []
    ##if quantile != "central": continue
    #window_values = quanDict.keys()
    #window_values.sort()
    ##for window_value,value in quanDict.iteritems():
    #for window_value in window_values:
    #    value = quanDict[window_value]
    #    x_list.append(window_value)
    #    y_xs_list.append(value*xs_dict[window_value])
    #    y_epsilon_list.append(epsilon*math.sqrt(value))
    #    y_br4l_list.append(value*xs_dict[window_value]/higgs_xs)
    #    y_brHZZd_list.append(value*xs_dict[window_value]/xs_brHZZd_dict[window_value])
    #    y_brHZX_XToll_list.append(value*xs_dict[window_value]/higgs_xs/z_2l_br/h_ZZ_br)
    #    #print window_value,value,xs_dict[window_value],value*xs_dict[window_value]
    #xArray = array.array('d',x_list)
    #yArray = array.array('d',y_xs_list)
    #espArray = array.array('d',y_epsilon_list)
    #br4lArray = array.array('d',y_br4l_list)
    #brHZZdArray = array.array('d',y_brHZZd_list)
    #brHZX_XTollArray = array.array('d',y_brHZX_XToll_list)
    #out_graph = ROOT.TGraph(nPoints,xArray,yArray)
    #out_epsilon_graph = ROOT.TGraph(nPoints,xArray,espArray)
    #out_br4l_graph = ROOT.TGraph(nPoints,xArray,br4lArray)
    #out_brHZZd_graph = ROOT.TGraph(nPoints,xArray,brHZZdArray)
    #out_brHZX_XToll_graph = ROOT.TGraph(nPoints,xArray,brHZX_XTollArray)
    #outGraphDict[quantile]["epsilon"] = out_epsilon_graph
    #outGraphDict[quantile]["BrHZZd"] = out_brHZZd_graph

#for quantile,quanDict in outGraphDict.iteritems():
#    outGraphDict[quantile]["epsilon"]

#c = ROOT.TCanvas()
#out_graph.Draw()
#c.SaveAs(option.outputPath.replace(".pdf","_xs.pdf"))
#
#c = ROOT.TCanvas()
#out_epsilon_graph.Draw()
#c.SaveAs(option.outputPath.replace(".pdf","_epsilon.pdf"))
#
#c = ROOT.TCanvas()
#out_br4l_graph.Draw()
#c.SaveAs(option.outputPath.replace(".pdf","_br4l.pdf"))
#
#c = ROOT.TCanvas()
#out_brHZZd_graph.Draw()
#c.SaveAs(option.outputPath.replace(".pdf","_brHZZd.pdf"))
#
#c = ROOT.TCanvas()
#out_brHZX_XToll_graph.Draw()
#c.SaveAs(option.outputPath.replace(".pdf","_brHZX_XToll.pdf"))
