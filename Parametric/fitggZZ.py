import ROOT

from ShapeFitter import ShapeFitter

ROOT.gROOT.SetBatch(ROOT.kTRUE)
ROOT.gSystem.Load("libHiggsAnalysisCombinedLimit.so")

inputPath           = "/raid/raid7/lucien/Higgs/DarkZ/ParaInput/DarkPhotonSelection_m4l118To130_Nominal/2018-11-21_DarkPhotonSR-Unblinding_Norm/ggZZ/StatInput.root"
outputPath          = "/home/lucien/public_html/Higgs/DarkZ/StatFW/2018-11-21_Parametrization/ggZZ_Poly.pdf"
ndof                = 4

argList = [
            ROOT.RooRealVar("c0","c0",  0.1,0.,5.),
            ROOT.RooRealVar("c1","c1",  0.,-2.,2.),
            ROOT.RooRealVar("c2","c2",  0.,-2.,2.),
            ROOT.RooRealVar("c3","c3",  0.,-1.,1.),
            ROOT.RooRealVar("c4","c4",  0.,-1.,1.),

            #ROOT.RooRealVar("c0","c0",  0.,-5.,5.),
            #ROOT.RooRealVar("c1","c1",  0.,-5.,5.),
            #ROOT.RooRealVar("c2","c2",  0.,-5.,5.),
            #ROOT.RooRealVar("c3","c3",  0.,-5.,5.),
            #ROOT.RooRealVar("c4","c4",  0.,-5.,5.),
            ] 

fitter = ShapeFitter("massZ2",0.,0.55)

pdf_poly = fitter.makePolyPdf("PolyPdf",argList)

pdf = pdf_poly

inputFile = ROOT.TFile(inputPath,"READ")
hist = inputFile.Get("comb-Norm")
hist.Rebin(10)
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
