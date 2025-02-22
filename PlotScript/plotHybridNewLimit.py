import ROOT,glob,os,argparse,subprocess,array,math
from collections import OrderedDict
import Utilities.CMS_lumi as CMS_lumi
import Utilities.tdrstyle as tdrstyle

from Physics.Zd_XS import *
from Physics.ALP_XS import *

ROOT.gROOT.SetBatch(ROOT.kTRUE)

parser = argparse.ArgumentParser()
parser.add_argument("--inputDir",action="store")
parser.add_argument("--outputPath",action="store")
parser.add_argument("--selectStr",action="store",default="")
parser.add_argument("--poi",action="store",default="")

option = parser.parse_args()

inputDir = option.inputDir

# ________________________________________________________________ ||
# CMS style
# ________________________________________________________________ ||
#CMS_lumi.cmsText = "CMS"
#CMS_lumi.extraText = "Preliminary"
CMS_lumi.cmsText = ""
CMS_lumi.extraText = ""
CMS_lumi.cmsTextSize = 0.65
CMS_lumi.outOfFrame = True
#CMS_lumi.lumi_13TeV = "77.3 fb^{-1}"
#CMS_lumi.lumi_13TeV = "35.9 fb^{-1}"
CMS_lumi.lumi_13TeV = "136.1 fb^{-1}"
#CMS_lumi.lumi_13TeV = "150 fb^{-1}"
tdrstyle.setTDRStyle()

setLogY         = False
#expOnly         = True 
#quantiles       = ["down2","down1","central","up1","up2","obs"]
quantiles       = ["obs"]
#quantiles       = ["down2","down1","central","up1","up2",]
varName         = "limit"
#plots           = ["epsilon","r","BrHZZd_Interpolation",]
#plots           = ["epsilon",]
#plots           = ["epsilon","r",]
#plots           = ["kappa","BrHZdZd_Interpolation"]
#plots           = ["epsilon_EpsPOI"]
#plots           = ["BrHZZd"]
#plots           = ["BrH4l",]
plots           = ["BrHZZd_Interpolation"] if not option.poi else option.poi.split(",")
maxFactor       = 1.2
y_label_dict    = {
                    "r": "Signal strength",
                    "epsilon": "#varepsilon",
                    "epsilon_EpsPOI": "#varepsilon",
                    "kappa": "#kappa",
                    "BrHZZd": "Br(h #rightarrow Z Z_{d})",
                    "BrHZZd_Interpolation": "Br(h #rightarrow Z Z_{d})",
                    "BrHZdZd": "Br(h #rightarrow Z_{d} Z_{d})",
                    "BrHZdZd_Interpolation": "Br(h #rightarrow Z_{d} Z_{d})",
                    "BrH4l": "Br(h #rightarrow ZX #rightarrow 4#mu)",
                    "c_zh_div_Lambda_Interpolation": "|C^{eff}_{Zh}|/#Lambda [TeV^{-1}]",
                    "c_ah_div_Lambda_Interpolation": "|C^{eff}_{ah}|/#Lambda^{2} [TeV^{-2}]",
                    "xs_ZZd": "Cross section [pb]",
                    "xs_ZdZd": "Cross section [pb]",
                    "BrHZX_BrXll": "Br(h #rightarrow Z X) #times Br(X #rightarrow ll)",
                    "BrHZX_BrXMuMu": "Br(h #rightarrow Z X) #times Br(X #rightarrow #mu #mu)",
                    "BrHZX_BrXee": "Br(h #rightarrow Z X) #times Br(X #rightarrow ee)",
                    "BrHXX_Br2Xll": "Br(h #rightarrow X X) #times Br(X #rightarrow ll)^{2}",
                    "BrHXX_Br2XMuMu": "Br(h #rightarrow X X) #times Br(X #rightarrow #mu #mu)^{2}",
                    "BrHXX_Br2Xee": "Br(h #rightarrow X X) #times Br(X #rightarrow ee)^{2}",
                    #"BrH4l": "Br(h #rightarrow ZX #rightarrow 4e)",
                  }
#x_label         = "m_{Z_{d}}"
x_label         = "m_{X}"
#x_label         = "m_{a}"
drawVetoBox     = True

def calculate(r_value,window_value,what):
    if what == "epsilon":
        return epsilon*math.sqrt(r_value)
    elif what == "kappa":
        return kappa*math.sqrt(r_value)
    elif what == "BrHZdZd":
        return r_value*xs_HZdZd_dict[window_value]/xs_brHZdZd_dict[window_value]
    elif what == "BrHZZd":
        return r_value*xs_dict[window_value]/xs_brHZZd_dict[window_value]
    elif what == "BrHZZd_Interpolation":
        return r_value*(higgs_xs*epsilon**2*reader.interpolate(window_value,"Br_HToZZdTo4l"))/(higgs_xs*reader.interpolate(window_value,"Br_ZdTo2l")*z_2l_br)
    elif what == "BrHZdZd_Interpolation":
        return r_value*(higgs_xs*kappa**2*reader.interpolate(window_value,"Br_HToZdZdTo4l"))/(higgs_xs*reader.interpolate(window_value,"Br_ZdTo2l")**2)
    elif what == "BrHZX_BrXll":
        return r_value*(epsilon**2*reader.interpolate(window_value,"Br_HToZZdTo4l"))/z_2l_br
    elif what == "BrHZX_BrXMuMu":
        return r_value*(epsilon**2*reader.interpolate(window_value,"Br_HToZZdTo4l"))/(z_2l_br/2.)
    elif what == "BrHZX_BrXee":
        return r_value*(epsilon**2*reader.interpolate(window_value,"Br_HToZZdTo4l"))/(z_2l_br/2.)
    elif what == "BrHXX_Br2Xll":
        return r_value*(kappa**2*reader.interpolate(window_value,"Br_HToZdZdTo4l"))
    elif what == "BrHXX_Br2XMuMu":
        return r_value*(kappa**2*reader.interpolate(window_value,"Br_HToZdZdTo4l"))
    elif what == "BrHXX_Br2Xee":
        return r_value*(kappa**2*reader.interpolate(window_value,"Br_HToZdZdTo4l"))
    elif what == "epsilon_EpsPOI":
        return r_value
    elif what == "BrH4l":
        return r_value*xs_dict[window_value]/higgs_xs
    elif what == "r":
        return r_value
    elif what == "xs_ZZd":
        return r_value*(higgs_boson.xs*epsilon**2*reader.interpolate(window_value,"Br_HToZZdTo4l"))
    elif what == "xs_ZdZd":
        return r_value*(higgs_boson.xs*kappa**2*reader.interpolate(window_value,"Br_HToZdZdTo4l"))
    elif what == "c_zh_div_Lambda_Interpolation":
        ratio_exc = r_value*(higgs_boson.xs*epsilon**2*reader.interpolate(window_value,"Br_HToZZdTo4l"))/higgs_boson.xs/z_boson.ll_br/ALP.ll_br
        Gamma_hToZa_exc = ratio_exc*higgs_boson.total_width/(1.-ratio_exc)
        return math.sqrt(Gamma_hToZa_exc*16.*math.pi/higgs_boson.mass**3/lambda_x_y_func((z_boson.mass/higgs_boson.mass)**2,(window_value/higgs_boson.mass)**2)**1.5)*1000
    elif what == "c_ah_div_Lambda_Interpolation":
        ratio_exc = r_value*(higgs_boson.xs*kappa**2*reader.interpolate(window_value,"Br_HToZdZdTo4l"))/higgs_boson.xs/ALP.ll_br/ALP.ll_br
        Gamma_hToaa_exc = ratio_exc*higgs_boson.total_width/(1.-ratio_exc)
        return math.sqrt(Gamma_hToaa_exc*32.*math.pi/higgs_boson.mass**3/higgs_boson.vev**2/(1.-2.*window_value**2/higgs_boson.mass**2)**2/math.sqrt(1.-4.*window_value**2/higgs_boson.mass**2))*1000*1000
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
    inputFile = ROOT.TFile(cardDir+"higgsCombineTest.HybridNew.mH120.root","READ")
    if inputFile.IsZombie(): continue
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
outputDir = os.path.dirname(option.outputPath)
if not os.path.exists(outputDir):
    os.makedirs(outputDir)
#nPoints = len(outDict["central"])
nPoints = len(outDict["obs"])
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
    CMS_lumi.CMS_lumi(c,4,11)
    #window_values = outDict["central"].keys()
    window_values = outDict["obs"].keys()
    window_values.sort()
    frame.GetXaxis().SetLimits(min(window_values),max(window_values))
    frameMax = max([calculate(outDict[quan][window_value],window_value,plot) for quan in quantiles for window_value in window_values ])*maxFactor
    frame.SetMaximum(frameMax)
    if setLogY: frame.SetMinimum(1E-5)
    for i,window_value in enumerate(window_values):
        if "up2" in outDict: yellow.SetPoint( i, window_value,calculate(outDict["up2"][window_value], window_value, plot) )
        if "down2" in outDict: yellow.SetPoint( 2*nPoints-1-i, window_value,calculate(outDict["down2"][window_value], window_value, plot) )
        if "up1" in outDict: green.SetPoint( i, window_value,calculate(outDict["up1"][window_value], window_value, plot) )
        if "down2" in outDict: green.SetPoint( 2*nPoints-1-i, window_value,calculate(outDict["down1"][window_value], window_value, plot) )
        if "central" in outDict: median.SetPoint( i, window_value,calculate(outDict["central"][window_value], window_value, plot) )
        if "obs" in outDict: black.SetPoint( i, window_value,calculate(outDict["obs"][window_value], window_value, plot) )
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

    c.SaveAs(option.outputPath.replace(".pdf","_"+plot+".pdf"))
