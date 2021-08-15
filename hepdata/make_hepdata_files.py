import os,ROOT,pickle

from StatFW.BaseObject import BaseObject

from hepdata_lib import Submission

ROOT.gROOT.SetBatch(ROOT.kTRUE)

out_name = 'hig19007_hepdata'

config = [
        BaseObject(
            "BrHXX_Br2Xee",
            plot = "BrHXX_Br2Xee",
            picklePath = os.environ["BASE_PATH"]+"/pickle/XX/2020-03-17_SR2D_RunII_El/limit.pkl",
            outputPath = "output/210816_v1/BrHXX_Br2Xee.C",
            method = "HybridNew",
            postfix = "_smooth",
            window_func = lambda x: x < 8.0 or x > 11.5,
            ), 
        BaseObject(
            "BrHXX_Br2Xmumu",
            plot = "BrHXX_Br2XMuMu",
            picklePath = os.environ["BASE_PATH"]+"/pickle/XX/2020-03-17_SR2D_RunII_Mu/limit.pkl",
            outputPath = "output/210816_v1/BrHXX_Br2Xmumu.C",
            method = "HybridNew",
            postfix = "_smooth",
            window_func = lambda x: x < 8.0 or x > 11.5,
            ),
        BaseObject(
            "BrHXX_Br2Xll",
            plot = "BrHXX_Br2Xll",
            picklePath = os.environ["BASE_PATH"]+"/pickle/XX/2020-03-17_SR2D_RunII/limit.pkl",
            outputPath = "output/210816_v1/BrHXX_Br2Xll.C",
            method = "HybridNew",
            postfix = "_smooth",
            window_func = lambda x: x < 8.0 or x > 11.5,
            ),
        BaseObject(
            "BrHZX_BrXee",
            plot = "BrHZX_BrXee",
            picklePath = os.environ["BASE_PATH"]+"/pickle/ZX/2020-03-03_CutAndCount_m4lSR-HZZd_RunII_El/limit.pkl",
            outputPath = "output/210816_v1/BrHZX_BrXee.C",
            method = "AsymptoticLimits",
            postfix = "",
            window_func = lambda x: x < 8.0 or x > 11.5,
            ),
        BaseObject(
            "BrHZX_BrXmumu",
            plot = "BrHZX_BrXMuMu",
            picklePath = os.environ["BASE_PATH"]+"/pickle/ZX/2020-03-03_CutAndCount_m4lSR-HZZd_RunII_Mu/limit.pkl",
            outputPath = "output/210816_v1/BrHZX_BrXmumu.C",
            method = "AsymptoticLimits",
            postfix = "",
            window_func = lambda x: x < 8.0 or x > 11.5,
            ),
        BaseObject(
            "BrHZX_BrXll",
            plot = "BrHZX_BrXll",
            picklePath = os.environ["BASE_PATH"]+"/pickle/ZX/2020-03-03_CutAndCount_m4lSR-HZZd_RunII/limit.pkl",
            outputPath = "output/210816_v1/BrHZX_BrXll.C",
            method = "AsymptoticLimits",
            postfix = "",
            window_func = lambda x: x < 8.0 or x > 11.5,
            ),
        BaseObject(
            "cah",
            plot = "c_ah_div_Lambda_Interpolation",
            picklePath = os.environ["BASE_PATH"]+"/pickle/XX/2020-03-17_SR2D_RunII/limit.pkl",
            outputPath = "output/210816_v1/cah.C",
            method = "HybridNew",
            postfix = "_smooth",
            window_func = lambda x: x < 8.0 or x > 11.5,
            ),
        BaseObject(
            "cZh",
            plot = "c_zh_div_Lambda_Interpolation",
            picklePath = os.environ["BASE_PATH"]+"/pickle/ZX/2020-03-03_CutAndCount_m4lSR-HZZd_RunII/limit.pkl",
            outputPath = "output/210816_v1/cZh.C",
            method = "AsymptoticLimits",
            postfix = "",
            window_func = lambda x: (x < 8.0 or x > 11.5) and x > 4.2 and x < 34.,
            ),
        BaseObject(
            "kappa",
            plot = "kappa",
            picklePath = os.environ["BASE_PATH"]+"/pickle/XX/2020-03-17_SR2D_RunII/limit.pkl",
            outputPath = "output/210816_v1/kappa.C",
            method = "HybridNew",
            postfix = "_smooth",
            window_func = lambda x: x < 8.0 or x > 11.5,
            ),
        ]

for c in config:
    c.setLogY = True
    c.y_min = 4E-7
    c.maxFactor = 10
    c.max_force = 4E-5
    c.x_label = "m_{X} [GeV]"
    c.leg_pos = [0.25,0.65,0.72,0.87]
    c.drawVetoBox = False
    c.drawLegend = True
    c.x_var = 'mass'
    c.x_unit = 'GeV'
    c.y_var = c.name
    c.y_unit = ''
    c.lumi = 137.

def read_limit_from_pickle(picklePath):
    outDict = pickle.load(open(picklePath,"r")) 
    return outDict

def draw_limit_with_dict(config,outDict):
    from PlotScript.plotLimitUtils import *
    outputPath = config.outputPath
    window_func = config.window_func
    maxFactor = config.maxFactor
    max_force = config.max_force
    setLogY = config.setLogY
    method = config.method
    y_min = config.y_min
    x_label = config.x_label
    leg_pos = config.leg_pos
    drawVetoBox = config.drawVetoBox
    drawLegend = config.drawLegend
    postfix = config.postfix
    plot = config.plot

    outputDir = os.path.dirname(outputPath)
    if not os.path.exists(outputDir):
        os.makedirs(outputDir)
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
    frame.GetYaxis().SetTitle(y_label_dict[plot])
    frame.GetXaxis().SetTitle(x_label)
    frame.SetMinimum(0)
    CMS_lumi.CMS_lumi(c,4,0)

    window_values = [m for m in outDict["central"].keys() if window_func(m)]
    window_values.sort()

    frame.GetXaxis().SetLimits(min(window_values),max(window_values))
    frameMax = max([calculate(outDict[quan.name][window_value],window_value,plot) for quan in quantiles for window_value in outDict[quan.name].keys() ])*maxFactor if not max_force else max_force
    frame.SetMaximum(frameMax)
    if setLogY: frame.SetMinimum(y_min)
    
    nPoints = len(window_values)
    black_xs = array.array("d",window_values)
    black_ys = array.array("d",[calculate(outDict["obs"][window_value],window_value,plot) for i,window_value in enumerate(window_values)])
    median_xs = array.array("d",window_values)
    median_ys = array.array("d",[calculate(outDict["central"+postfix][window_value],window_value,plot) for i,window_value in enumerate(window_values)])
    
    yellow_ns_list = []
    yellow_xs_list = []
    yellow_up_ys_list = []
    yellow_down_ys_list = []
    for i,window_value in enumerate(window_values):
        yellow_ns_list.append(i)
        yellow_xs_list.append(window_value)
        yellow_up_ys_list.append(calculate(outDict["up2"+postfix][window_value], window_value, plot))
    for i,window_value in enumerate(window_values):
        yellow_xs_list.append(window_value)
        yellow_down_ys_list.append(calculate(outDict["down2"+postfix][window_value], window_value, plot))
    
    green_ns_list = []
    green_xs_list = []
    green_up_ys_list = []
    green_down_ys_list = []
    for i,window_value in enumerate(window_values):
        green_ns_list.append(i)
        green_xs_list.append(window_value)
        green_up_ys_list.append(calculate(outDict["up1"+postfix][window_value], window_value, plot))
    for i,window_value in enumerate(window_values):
        green_xs_list.append(window_value)
        green_down_ys_list.append(calculate(outDict["down1"+postfix][window_value], window_value, plot))
    
    yellow_xs = array.array("d",yellow_xs_list)
    yellow_up_ys = array.array("d",yellow_up_ys_list)
    yellow_down_ys = array.array("d",yellow_down_ys_list)
    green_xs = array.array("d",green_xs_list)
    green_up_ys = array.array("d",green_up_ys_list)
    green_down_ys = array.array("d",green_down_ys_list)
    
    yellow_up = ROOT.TGraph(nPoints,yellow_xs,yellow_up_ys)
    yellow_down = ROOT.TGraph(nPoints,yellow_xs,yellow_down_ys)
    green_up = ROOT.TGraph(nPoints,green_xs,green_up_ys)
    green_down = ROOT.TGraph(nPoints,green_xs,green_down_ys)
    median = ROOT.TGraph(nPoints,median_xs,median_ys)
    black = ROOT.TGraph(nPoints,black_xs,black_ys)
    
    yellow_up.Draw('L') 
    green_up.Draw('Lsame')

    median.SetLineColor(1)
    median.SetLineWidth(2)
    median.SetLineStyle(2)
    median.Draw('Lsame')
    
    black.SetLineColor(1)
    black.SetLineWidth(2)
    black.SetLineStyle(1)
    black.Draw("Lsame")
    
    green_down.Draw('Lsame')
    yellow_down.Draw('Lsame') 

    ROOT.gPad.RedrawAxis()
    ROOT.gPad.RedrawAxis("G")
            
    c.SaveAs(outputPath)

def add_limit_to_submission(c,submission):
    from hepdata_lib import Table
    from hepdata_lib.c_file_reader import CFileReader
    from hepdata_lib import Variable, Uncertainty
    
    table = Table(c.y_var)
    table.description = 'Exclusion limit for '+c.y_var

    reader = CFileReader(c.outputPath)
    graphs = reader.get_graphs()

    d = Variable(c.x_var, is_independent=True, is_binned=False, units=c.x_unit)
    d.values = graphs["Graph2"]['x']

    obs = Variable(c.y_var, is_independent=False, is_binned=False, units=c.y_unit)
    obs.values = graphs["Graph3"]['y']
    obs.add_qualifier("Limit", "Observed")

    exp = Variable(c.y_var, is_independent=False, is_binned=False, units=c.y_unit)
    exp.values = graphs["Graph2"]['y']
    exp.add_qualifier("Limit", "Expected")

    up2 = Variable(c.y_var, is_independent=False, is_binned=False, units=c.y_unit)
    up2.values = graphs["Graph0"]['y']
    up2.add_qualifier("Limit", "+2sigma")

    up1 = Variable(c.y_var, is_independent=False, is_binned=False, units=c.y_unit)
    up1.values = graphs["Graph1"]['y']
    up1.add_qualifier("Limit", "+1sigma")

    down1 = Variable(c.y_var, is_independent=False, is_binned=False, units=c.y_unit)
    down1.values = graphs["Graph4"]['y']
    down1.add_qualifier("Limit", "-1sigma")

    down2 = Variable(c.y_var, is_independent=False, is_binned=False, units=c.y_unit)
    down2.values = graphs["Graph5"]['y']
    down2.add_qualifier("Limit", "-2sigma")

    table.add_variable(d)
    table.add_variable(up2)
    table.add_variable(up1)
    table.add_variable(obs)
    table.add_variable(exp)
    table.add_variable(down1)
    table.add_variable(down2)
    submission.add_table(table)

if __name__ == "__main__":
    submission = Submission()
    
    for c in config:
        outdict = read_limit_from_pickle(c.picklePath)
        draw_limit_with_dict(c,outdict)
        add_limit_to_submission(c,submission)
    
    submission.create_files(out_name)
