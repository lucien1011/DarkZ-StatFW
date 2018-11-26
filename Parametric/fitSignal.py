import ROOT

from ShapeFitter import ShapeFitter

ROOT.gROOT.SetBatch(ROOT.kTRUE)
ROOT.gSystem.Load("libHiggsAnalysisCombinedLimit.so")

inputPath           = "/raid/raid7/lucien/Higgs/DarkZ/ParaInput/DarkPhotonSelection_m4l118To130_Nominal/2018-11-21_DarkPhotonSR-Unblinding_Norm/HZZd_M7/StatInput.root"
outputPath          = "/home/lucien/public_html/Higgs/DarkZ/StatFW/2018-11-21_Parametrization/HZZd_M7_BW.pdf"

fitter = ShapeFitter("massZ2",0.,0.55)
pdf,meanVar,widthVar = fitter.makeBreitWignerPdf("BWPdf","mean",0.,0.55,"width",0.,300.)

inputFile = ROOT.TFile(inputPath,"READ")
hist = inputFile.Get("comb-Norm")
yieldVar = ROOT.RooRealVar("Yield","Yield", 0, 40)
data = ROOT.RooDataHist("data","data",ROOT.RooArgList(fitter.obsVar,yieldVar),hist)

result = pdf.fitTo(data)

c = ROOT.TCanvas("c1","c1",800,800)
c.cd()
plot = fitter.obsVar.frame()
data.plotOn(plot,ROOT.RooFit.Name("data"))
pdf.plotOn(plot,ROOT.RooFit.Name("Parametric"))
plot.Draw()
c.SaveAs(outputPath)
