import ROOT

from ShapeFitter import ShapeFitter

ROOT.gROOT.SetBatch(ROOT.kTRUE)
ROOT.gSystem.Load("libHiggsAnalysisCombinedLimit.so")

inputPath           = "/raid/raid7/lucien/Higgs/DarkZ/ParaInput/DarkPhotonSelection_m4l118To130_Nominal/2018-11-21_DarkPhotonSR-Unblinding_Norm/Higgs/StatInput.root"
outputPath          = "/home/lucien/public_html/Higgs/DarkZ/StatFW/2018-11-21_Parametrization/Higgs_Poly.pdf"
ndof                = 8

argList = [
            ROOT.RooRealVar("c0","c0",  0.1,0.,5.),
            ROOT.RooRealVar("c1","c1",  0.,0.,2.),
            ROOT.RooRealVar("c2","c2",  0.,-5.,0.),
            ROOT.RooRealVar("c3","c3",  0.,-1.,1.),
            ROOT.RooRealVar("c4","c4",  0.,-1.,1.),

            #ROOT.RooRealVar("c0","c0",  0.,-5.,5.),
            #ROOT.RooRealVar("c1","c1",  0.,-5.,5.),
            #ROOT.RooRealVar("c2","c2",  0.,-5.,5.),
            #ROOT.RooRealVar("c3","c3",  0.,-5.,5.),
            #ROOT.RooRealVar("c4","c4",  0.,-5.,5.),
            ] 

fitter = ShapeFitter("massZ2",0.,0.55)

pdf_landau,meanVar,widthVar = fitter.makeLandauPdf("LandauPdf","meanLandau",0.,120.,"widthLandau",0.,300.)
pdf_gaus,meanGausVar,widthGausVar = fitter.makeGausPdf("GausPdf","meanGaus",0.,120.,"widthGaus",0.,300.)
pdf_bifurGaus,meanGausVar,widthLeftVar,widthRightVar = fitter.makeBifurGausPdf("GausPdf","meanBifurGaus",0.,1.,"widthBifurGaus",0.,300.,0.,300.)
pdf_CB,meanCBVar,widthCBVar,alphaCBVar,nCBVar = fitter.makeCBPdf("CBPdf","meanCB",0.,1.,"widthCB",0.,1.,"alphaCB",-1.,1.,"nCB",-1.,1.)
pdf_che = fitter.makeChebychevPdf("HiggsPdf",argList)
pdf_bern = fitter.makeBernPdf("HiggsPdf",argList)
pdf_poly = fitter.makePolyPdf("PolyPdf",argList)
pdf_chi2,nChi2Var = fitter.makeChiSquarePdf("Chi2Pdf","nChi2",0.,10.)
pdf_exp,widthExpVar = fitter.makeExpPdf("ExpPdf","widthExp",-300.,300.)

#pdf,coeffVar = fitter.addPdf("AddPdf",pdf_bifurGaus,pdf_chi2)
#pdf = fitter.prodPdf("ProdPdf",pdf_gaus,pdf_poly)
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

#fitter.end()
