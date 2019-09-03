import ROOT,argparse,sys,os
from collections import OrderedDict

# __________________________________________________________________________________________________________ ||
def makePlot(nuisDict,whichFit,histName="postFitNuisance",labelFunc=None):
    nNuis = len(nuisDict)
    hist = ROOT.TH1D(histName,"Nuisance parameters",nNuis,0,nNuis)
    iNuis = 1
    for nuisName,nuisTuple in nuisDict.iteritems():
        if whichFit == "postfit":
            nuisValue,nuisErr = nuisTuple
            hist.SetBinContent(iNuis,nuisValue)
            hist.SetBinError(iNuis,nuisErr)
        else:
            hist.SetBinContent(iNuis,0.)
            hist.SetBinError(iNuis,1.)
        hist.GetXaxis().SetBinLabel(iNuis,nuisName if not labelFunc else labelFunc(nuisName))
        iNuis += 1
    return hist

def plotStyle(hist,color=ROOT.kBlue):
    hist.GetYaxis().SetTitle("#theta - #theta_{0}")
    hist.SetLineColor(color)
    hist.SetMarkerStyle(20)
    hist.SetMarkerSize(1.0)
    hist.SetLineWidth(2)
    hist.GetXaxis().LabelsOption("v")
    hist.SetMaximum(3.)
    hist.SetMinimum(-3.)
    #hist.SetStats(0)
    hist.SetMarkerColor(color)

def getGraph(hist,shift):
    gr = ROOT.TGraphErrors()
    gr.SetName(hist.GetName())
    for i in range(hist.GetNbinsX()):
        x = hist.GetBinCenter(i+1)+shift
        y = hist.GetBinContent(i+1)
        e = hist.GetBinError(i+1)
        gr.SetPoint(i,x,y)
        gr.SetPointError(i,float(abs(shift))*0.1,e)
    return gr

# __________________________________________________________________________________________________________ ||
parser = argparse.ArgumentParser()

parser.add_argument('--inputPath',action='store')
parser.add_argument('--outputPath',action='store')
parser.add_argument('--verbose',action='store_true')
parser.add_argument('--fitResultName',action='store')

option = parser.parse_args()

ROOT.gROOT.SetBatch(ROOT.kTRUE)
ROOT.gStyle.SetOptStat(0)

# __________________________________________________________________________________________________________ ||
inputFile = ROOT.TFile(option.inputPath,"READ")
fitResult = inputFile.Get("fit_b" if not option.fitResultName else option.fitResultName).floatParsFinal()

nuisDict = OrderedDict()
for i in range(fitResult.getSize()):
    nuis = fitResult.at(i)
    nuisName = nuis.GetName()
    if nuisName == "r": continue
    if option.verbose: print "Processing ",nuisName
    nuisDict[nuisName] = (nuis.getVal(),nuis.getError())

# __________________________________________________________________________________________________________ ||
#postFitHist = makePlot(nuisDict,"postfit")
#preFitHist = makePlot(nuisDict,"prefit")
#postFitPlot = getGraph(postFitHist,0.)
#preFitPlot = getGraph(preFitHist,0.)
postFitPlot = makePlot(nuisDict,"postfit")
preFitPlot = makePlot(nuisDict,"prefit")
plotStyle(postFitPlot,color=ROOT.kBlue)
plotStyle(preFitPlot,color=ROOT.kBlack)
postFitPlot.GetYaxis().SetRangeUser(-3.,3.)
preFitPlot.GetYaxis().SetRangeUser(-3.,3.)
c = ROOT.TCanvas()
preFitPlot.SetFillColor(ROOT.kGray)
preFitPlot.SetMarkerSize(0.001)
preFitPlot.Draw("E2")
preFitPlot.GetXaxis().SetLabelSize(0.02)
postFitPlot.GetXaxis().SetLabelSize(0.02)
postFitPlot.Draw("Esame")
c.SetGridx()
c.SetGridy()
c.RedrawAxis('g')
if not os.path.exists(os.path.dirname(os.path.abspath(option.outputPath))):
    os.makedirs(os.path.dirname(os.path.abspath(option.outputPath)))
c.SaveAs(option.outputPath)

# __________________________________________________________________________________________________________ ||
