import ROOT,os
from StatFW.BaseObject import BaseObject
from Utils.mkdir_p import mkdir_p

ROOT.gROOT.SetBatch(ROOT.kTRUE)

# ________________________________________________________________________________ ||
inputDir1       = "HToZdZd_DataCard/2019-12-06_SR_RunII/"
inputDir2       = "HToZdZd_DataCard/2019-12-06_SR2D_RunII/"
mass_points     = [4,5,6,7,8,9,10,15,20,25,30,35,40,45,50,55,60,]
dirTemplate     = "Zd_MZD%s"
textFileName    = "AsymptoticLimits_Out.txt"
lineStr         = "Expected 50.0%"
outPlotPath     = "/home/lucien/public_html/Higgs/HToZdZd/Misc/LimitComparison/2019-12-06_RunII_SRvsSR2D/AsymptoticLimitRatio.pdf"
histName        = "LimitRatio"
title           = "; m_{Z_{d}} (GeV); Limit ratio"

# ________________________________________________________________________________ ||
outPoints = []
if outPlotPath: mkdir_p(os.path.dirname(outPlotPath))
for m in mass_points:
    textFilePath1 = os.path.join(inputDir1,dirTemplate%m,textFileName)
    textFile1 = open(textFilePath1,"r")
    lines1 = textFile1.readlines()
    foundLine1 = False
    for line1 in lines1: 
        if line1.startswith(lineStr): 
            foundLine1 = True
            break
    textFilePath2 = os.path.join(inputDir2,dirTemplate%m,textFileName)
    textFile2 = open(textFilePath2,"r")
    lines2 = textFile2.readlines()
    foundLine2 = False
    for line2 in lines2: 
        if line2.startswith(lineStr):
            foundLine2 = True
            break
    if not foundLine1 or not foundLine2: continue
    limit1 = float(line1.split()[-1])
    limit2 = float(line2.split()[-1])
    point = BaseObject(dirTemplate%m,mass=m,limit1=limit1,limit2=limit2)
    outPoints.append(point)
    print "Mass %s: %4.2f %%"%(m,(1.-limit2/limit1)*100)
if outPlotPath:
    c = ROOT.TCanvas()
    hist = ROOT.TH1D(histName,title,len(outPoints),-0.5,len(outPoints)-0.5)
    for i,p in enumerate(outPoints):
        hist.SetBinContent(i+1,p.limit2/p.limit1)
        hist.GetXaxis().SetBinLabel(i+1,str(p.mass))
    hist.SetStats(0)
    hist.Draw()
    c.SaveAs(outPlotPath)
