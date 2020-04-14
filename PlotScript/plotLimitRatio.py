from PlotScript.plotLimitUtils import *

ROOT.gROOT.SetBatch(ROOT.kTRUE)

# ________________________________________________________________ ||
inputDir2       = "/cms/data/store/user/t2/users/klo/HiggsCombine/2020-03-03_CutAndCount_m4lSR-HZZd_RunII_LHCLimit_v2/"
inputDir1       = "/cms/data/store/user/klo/HiggsCombineWorkspace/HIG-19-007/ZX_2020-03-03_CutAndCount_m4lSR-HZZd_RunII/"
outputPath      = "/home/kinho.lo/public_html/Higgs/DarkZ/Misc/2020-03-03_CutAndCount_m4lSR-HZZd_RunII_LimitRatio.pdf"
selectStr       = ""
quan            = "central"
massCutFunc     = lambda x: x > 4.2
frameMax        = 1.5
frameMin        = 0.5

# ________________________________________________________________ ||
outDict1 = makeLimitDict(inputDir1,selectStr,"AsymptoticLimits",massCutFunc)
outDict2 = makeLimitDict(inputDir2,selectStr,"HybridNew",massCutFunc)
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
frame.SetMinimum(frameMin)
frame.SetMaximum(frameMax)
frame.GetYaxis().CenterTitle()
frame.GetYaxis().SetTitleSize(0.05)
frame.GetXaxis().SetTitleSize(0.05)
frame.GetXaxis().SetLabelSize(0.04)
frame.GetYaxis().SetLabelSize(0.03)
frame.GetYaxis().SetTitleOffset(1.2)
frame.GetXaxis().SetNdivisions(508)
nPoints = len(outDict1[quan])
black = ROOT.TGraph(nPoints)
window_values = outDict1[quan].keys()
window_values.sort()
frame.GetXaxis().SetLimits(min(window_values),max(window_values))
for i,window_value in enumerate(window_values):
    if window_value == 6.65254070815: 
        black.SetPoint(i,window_value,1.)
        continue
    black.SetPoint(i,window_value,outDict1[quan][window_value]/outDict2[quan][window_value])
black.SetLineColor(1)
black.SetLineWidth(2)
black.SetLineStyle(1)
black.Draw()
box = ROOT.TBox(lowBoxCut,0.,highBoxCut,frameMax)
box.SetFillColor(ROOT.kGray)
box.Draw('same')
outputDir = os.path.dirname(outputPath)
if not os.path.exists(outputDir):
    os.makedirs(outputDir)
c.SaveAs(outputPath)
