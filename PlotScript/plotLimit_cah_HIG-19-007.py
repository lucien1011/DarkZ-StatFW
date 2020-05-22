from PlotScript.plotLimitUtils import *

ROOT.gROOT.SetBatch(ROOT.kTRUE)

#inputDir = "/home/lucien/AnalysisCode/Higgs/DarkZ-StatFW-2/HToZdZd_DataCard/2019-12-17_SR2D_RunII/"
#outputPath = "/home/lucien/public_html/Higgs/HToZdZd/Limit/2020-02-26_SR2D_RunII/ExpObsLimit.pdf" 
#selectStr = ""

#inputDir = "/home/lucien/AnalysisCode/Higgs/DarkZ-StatFW/HToZdZd_DataCard/2020-03-03_SR2D_RunII/"
#outputPath = "/home/lucien/public_html/Higgs/HToZdZd/Limit/2020-03-03_SR2D_RunII/ExpObsLimit.pdf" 
#selectStr = ""

#inputDir = "/home/lucien/AnalysisCode/Higgs/DarkZ-StatFW/HToZdZd_DataCard/2020-03-06_SR2D_RunII/"
#outputPath = "/home/lucien/public_html/Higgs/HToZdZd/Limit/2020-03-06_SR2D_RunII/ExpObsLimit.pdf" 
#selectStr = ""

#inputDir = "/home/lucien/AnalysisCode/Higgs/DarkZ-StatFW/HToZdZd_DataCard/2020-03-17_SR2D_RunII/"
#outputPath = "/home/lucien/public_html/Higgs/HToZdZd/Limit/2020-03-17_SR2D_RunII/ExpObsLimit.pdf" 
#selectStr = ""

#inputDir = "/cms/data/store/user/t2/users/klo/HiggsCombine/2020-03-17_SR2D_RunII_LHCLimit/"
#outputPath = "/home/kinho.lo/public_html/Higgs/HToZdZd/Limit/2020-03-17_SR2D_RunII_LHCLimit/ExpObsLimit.pdf"
#selectStr = ""

#inputDir = "/cms/data/store/user/t2/users/klo/HiggsCombine/2020-03-17_SR2D_RunII_LHCLimit_v2/"
#outputPath = "/home/kinho.lo/public_html/Higgs/HToZdZd/Limit/2020-03-17_SR2D_RunII_LHCLimit_v2/ExpObsLimit.pdf"
#selectStr = ""

inputDir = "/raid/raid7/lucien/UFTier2/HiggsCombine/2020-03-17_SR2D_RunII_LHCLimit_v2/"
outputPath = "/home/lucien/public_html/Higgs/HToZdZd/Limit/2020-03-17_SR2D_RunII_LHCLimit_v2/ExpObsLimit.pdf"
selectStr = ""
dcDir = "/home/lucien/AnalysisCode/Higgs/DarkZ-StatFW/HToZdZd_DataCard/2020-03-17_SR2D_RunII/"

# ________________________________________________________________ ||
# CMS style
# ________________________________________________________________ ||
setLogY         = True
method          = "HybridNew"
#method          = "AsymptoticLimits"
varName         = "limit"
plot            = "c_ah_div_Lambda_Interpolation"
y_min           = 5E-3
maxFactor       = 10
max_force       = 0.1
x_label         = "m_{a} [GeV]"
drawVetoBox     = True
massCutFunc     = lambda x: x < 60.2
smoothing       = True
leg_pos         = [0.40,0.65,0.75,0.87]
drawLegend      = True

# ________________________________________________________________ ||
# Read limit from directory
# ________________________________________________________________ ||
outDict = makeLimitDict(inputDir,selectStr,method,massCutFunc,smoothing=smoothing,dcDir=dcDir,)

# ________________________________________________________________ ||
# Draw limit with outDict
# ________________________________________________________________ ||
outputDir = os.path.dirname(outputPath)
if not os.path.exists(outputDir):
    os.makedirs(outputDir)
nPoints = len(outDict["central"])
outGraphDict = {}
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
frame.GetXaxis().SetLabelSize(0.05)
frame.GetYaxis().SetLabelSize(0.05)
frame.GetYaxis().SetTitleOffset(1.0)
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
frameMax = max([calculate(outDict[quan.name][window_value],window_value,plot) for quan in quantiles for window_value in outDict[quan.name].keys() ])*maxFactor if not max_force else max_force
frame.SetMaximum(frameMax)
if setLogY: frame.SetMinimum(y_min)
for i,window_value in enumerate(window_values):
    postfix = "" if not smoothing else "_smooth"
    yellow.SetPoint( i, window_value,calculate(outDict["up2"+postfix][window_value], window_value, plot) )
    yellow.SetPoint( 2*nPoints-1-i, window_value,calculate(outDict["down2"+postfix][window_value], window_value, plot) )
    green.SetPoint( i, window_value,calculate(outDict["up1"+postfix][window_value], window_value, plot) )
    green.SetPoint( 2*nPoints-1-i, window_value,calculate(outDict["down1"+postfix][window_value], window_value, plot) )
    median.SetPoint( i, window_value,calculate(outDict["central"][window_value], window_value, plot) )
    black.SetPoint( i, window_value,calculate(outDict["obs"][window_value], window_value, plot) )

if drawLegend:
    leg = ROOT.TLegend(*leg_pos)
    leg.SetBorderSize(0)
    leg.SetFillColor(0)
    leg.SetTextSize(0.05)
    leg.AddEntry(median,"Expected exclusion","l")
    leg.AddEntry(black,"Observed exclusion","l")

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

if drawLegend:
    leg.Draw("Lsame")

if setLogY:
    c.SetLogy()

ROOT.gPad.RedrawAxis()
ROOT.gPad.RedrawAxis("G")

if drawVetoBox:
    box = ROOT.TBox(lowBoxCut,0.,highBoxCut,frameMax)
    box.SetFillColor(ROOT.kGray)
    box.Draw('same')

c.SaveAs(outputPath.replace(".pdf","_"+plot+".pdf"))
