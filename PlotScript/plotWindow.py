import ROOT,glob,os,argparse,subprocess,array,math
from collections import OrderedDict
import Utils.CMS_lumi as CMS_lumi
import Utils.tdrstyle as tdrstyle
from Utils.mkdir_p import mkdir_p

from Physics.Zd_XS import *
from StatFW.BaseObject import BaseObject

ROOT.gROOT.SetBatch(ROOT.kTRUE)

##__________________________________________________________________||
parser = argparse.ArgumentParser()
parser.add_argument("--inputDir",action="store")
parser.add_argument("--outputPath",action="store")
parser.add_argument("--method",action="store",default="AsymptoticLimits")

option = parser.parse_args()

inputDir = option.inputDir

##__________________________________________________________________||
expOnly         = True 
varName         = "limit"
method          = option.method
process         = "Zd"
#method          = "AsymptoticLimits"
#method          = "Significance"
select_entry    = {
                    "AsymptoticLimits": 2,
                    "Significance": 0,
                    }[method]
mass_points     = [
                        #BaseObject(process+"_MZD4" ,color=ROOT.kRed,latexName="Z_{d} = 4 GeV"),
                        #BaseObject(process+"_MZD10",color=ROOT.kBlue,latexName="Z_{d} = 10 GeV"),
                        #BaseObject(process+"_MZD15",color=ROOT.kViolet,latexName="Z_{d} = 15 GeV"),
                        #BaseObject(process+"_MZD20",color=ROOT.kGreen,latexName="Z_{d} = 20 GeV"),
                        #BaseObject(process+"_MZD25",color=ROOT.kOrange,latexName="Z_{d} = 25 GeV"),
                        #BaseObject(process+"_MZD30",color=ROOT.kBlack,latexName="Z_{d} = 30 GeV"),

                        BaseObject(process+"_MZD4" ,color=ROOT.kRed,latexName="Z_{d} = 4 GeV"),
                        BaseObject(process+"_MZD10",color=ROOT.kBlue,latexName="Z_{d} = 10 GeV"),
                        BaseObject(process+"_MZD20",color=ROOT.kViolet,latexName="Z_{d} = 20 GeV"),
                        BaseObject(process+"_MZD30",color=ROOT.kGreen,latexName="Z_{d} = 30 GeV"),
                        BaseObject(process+"_MZD40",color=ROOT.kOrange,latexName="Z_{d} = 40 GeV"),
                        BaseObject(process+"_MZD50",color=ROOT.kBlack,latexName="Z_{d} = 50 GeV"),                  
                        BaseObject(process+"_MZD60",color=ROOT.kYellow+2,latexName="Z_{d} = 60 GeV"),                  
                        ]
mass_value_func = lambda x: int(x.split("_")[1].replace("MZD",""))
#x_value_func    = lambda x: float(x.split("_")[0].replace("Mu","").replace("p","."))
#x_value_func    = lambda x: float(x.split("_")[1].replace("El","").replace("p","."))
x_value_func    = lambda x: float(x)
array_type      = 'd'
leg_pos         = [0.70,0.45,0.89,0.57]

##__________________________________________________________________||
outDict = OrderedDict()
for mass_point in mass_points:
    outDict[mass_point] = OrderedDict()
    for windowDir in glob.glob(inputDir+"*/"+mass_point.name+"/"):
        print "Reading directory "+windowDir
        window = windowDir.split("/")[-3]
        inputFile = ROOT.TFile(windowDir+"higgsCombineTest."+method+".mH120.root","READ")
        tree = inputFile.Get(varName)
        mass_value = mass_value_func(mass_point.name)
        x_value = x_value_func(window)
        outDict[mass_point][x_value] = []
        if expOnly:
            for i,entry in enumerate(tree):
                outDict[mass_point][x_value].append(getattr(entry,varName))
        else:
            raise RuntimeError

##__________________________________________________________________||
mkdir_p(os.path.dirname(option.outputPath))
c = ROOT.TCanvas()
mg = ROOT.TMultiGraph()
for i,mass_point in enumerate(mass_points):
    x_points = []
    y_points = []
    n = len(outDict[mass_point])
    x_values_list = outDict[mass_point].keys()
    x_values_list.sort()
    for x_value in x_values_list:
        y_value = outDict[mass_point][x_value][select_entry]
        x_points.append(x_value)
        y_points.append(y_value)
    gr = ROOT.TGraph(n,array.array(array_type,x_points),array.array(array_type,y_points))
    gr.SetName(mass_point.name)
    gr.SetTitle(mass_point.latexName)
    mg.Add(gr)
    gr.SetLineColor(mass_point.color)
mg.Draw("A")
c.BuildLegend(*leg_pos)
c.SaveAs(option.outputPath)
