from PlotScript.plotLimitUtils import *

ROOT.gROOT.SetBatch(ROOT.kTRUE)

picklePath = os.environ["BASE_PATH"]+"/pickle/XX/2020-03-17_SR2D_RunII_Mu/limit.pkl"

outputPath = "output/210806_v1/BrHXX_Br2Xmumu.C"


setLogY         = True
#expOnly         = True 
method          = "HybridNew"
#method          = "AsymptoticLimits"
varName         = "limit"
plot            = "BrHXX_Br2XMuMu"
y_min           = 4E-7
maxFactor       = 10
max_force       = 4E-5
x_label         = "m_{X} [GeV]"
leg_pos         = [0.30,0.65,0.90,0.87]
drawVetoBox     = True
drawLegend      = True
massCutFunc     = lambda x: x < 60.2
smoothing       = True
graphs          = [
        BaseObject("g1",window_func=lambda x: x < lowBoxCut),
        BaseObject("g2",window_func=lambda x: x > highBoxCut),
        ]

# ________________________________________________________________ ||
# Read limit from directory
# ________________________________________________________________ ||
outDict = pickle.load(open(picklePath,"r")) 

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
frame.GetYaxis().SetTitleOffset(1.2)
frame.GetXaxis().SetTitleOffset(1.0)
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

for g in graphs:
    postfix = "" if not smoothing else "_smooth"
    nPoints = len([w for w in window_values if g.window_func(w)])
    black_xs = array.array("d",[window_value for i,window_value in enumerate(window_values) if g.window_func(window_value)])
    black_ys = array.array("d",[calculate(outDict["obs"+postfix][window_value],window_value,plot) for i,window_value in enumerate(window_values) if g.window_func(window_value)])
    median_xs = array.array("d",[window_value for i,window_value in enumerate(window_values) if g.window_func(window_value)])
    median_ys = array.array("d",[calculate(outDict["central"+postfix][window_value],window_value,plot) for i,window_value in enumerate(window_values) if g.window_func(window_value)])

    yellow_ns_list = []
    yellow_xs_list = []
    yellow_ys_list = []
    for i,window_value in enumerate(window_values):
        if not g.window_func(window_value): continue
        yellow_ns_list.append(i)
        yellow_xs_list.append(window_value)
        yellow_ys_list.append(calculate(outDict["up2"+postfix][window_value], window_value, plot))
    for i,window_value in enumerate(reversed(window_values)):
        if not g.window_func(window_value): continue
        yellow_xs_list.append(window_value)
        yellow_ys_list.append(calculate(outDict["down2"+postfix][window_value], window_value, plot))

    green_ns_list = []
    green_xs_list = []
    green_ys_list = []
    for i,window_value in enumerate(window_values):
        if not g.window_func(window_value): continue
        green_ns_list.append(i)
        green_xs_list.append(window_value)
        green_ys_list.append(calculate(outDict["up1"+postfix][window_value], window_value, plot))
    for i,window_value in enumerate(reversed(window_values)):
        if not g.window_func(window_value): continue
        green_xs_list.append(window_value)
        green_ys_list.append(calculate(outDict["down1"+postfix][window_value], window_value, plot))

    yellow_xs = array.array("d",yellow_xs_list)
    yellow_ys = array.array("d",yellow_ys_list)
    green_xs = array.array("d",green_xs_list)
    green_ys = array.array("d",green_ys_list)

    g.yellow = ROOT.TGraph(2*nPoints,yellow_xs,yellow_ys)
    g.green = ROOT.TGraph(2*nPoints,green_xs,green_ys)
    g.median = ROOT.TGraph(nPoints,median_xs,median_ys)
    g.black = ROOT.TGraph(nPoints,black_xs,black_ys)

if drawLegend:
    leg = ROOT.TLegend(*leg_pos)
    leg.SetBorderSize(0)
    leg.SetFillColor(0)
    leg.SetTextSize(0.05)
    leg.AddEntry(g.median,"Expected exclusion","l",)
    leg.AddEntry(g.black,"Observed exclusion","l",)

for g in graphs:

    g.yellow.SetFillColor(ROOT.kOrange)
    g.yellow.SetLineColor(ROOT.kOrange)
    g.yellow.SetFillStyle(1001)
    g.yellow.Draw('F')
    
    g.green.SetFillColor(ROOT.kGreen+1)
    g.green.SetLineColor(ROOT.kGreen+1)
    g.green.SetFillStyle(1001)
    g.green.Draw('Fsame')

    g.median.SetLineColor(1)
    g.median.SetLineWidth(2)
    g.median.SetLineStyle(2)
    g.median.Draw('Lsame')

    g.black.SetLineColor(1)
    g.black.SetLineWidth(2)
    g.black.SetLineStyle(1)
    g.black.Draw("Lsame")

if setLogY:
    c.SetLogy()

ROOT.gPad.RedrawAxis()
ROOT.gPad.RedrawAxis("G")

if drawLegend:
    leg.Draw("Lsame")

if drawVetoBox:
    box = ROOT.TBox(lowBoxCut,0.,highBoxCut,frameMax)
    box.SetFillColor(ROOT.kGray)
    box.Draw('same')

c.SaveAs(outputPath)
