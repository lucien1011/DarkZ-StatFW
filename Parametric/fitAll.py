import os,ROOT

from ShapeFitter import ShapeFitter

# ___________________________________________________________________________________________ ||
pdfType_hist = "Hist"
pdfType_BW = "BreitWigner"
pdfType_poly = "Poly"
pdfType_landau = "Landau"
pdfType_data = "Data"

class Config(object):
    def __init__(self,**kwargs):
        self.__dict__.update(kwargs)

ROOT.gROOT.SetBatch(ROOT.kTRUE)
ROOT.gSystem.Load("libHiggsAnalysisCombinedLimit.so")

# ___________________________________________________________________________________________ ||
#inputDir                = "/raid/raid7/lucien/Higgs/DarkZ/ParaInput/DarkPhotonSelection_m4l118To130_Nominal/2018-11-21_DarkPhotonSR-Unblinding_Norm/"
inputDir                = "/raid/raid7/lucien/Higgs/DarkZ/ParaInput/DarkPhotonSelection_m4l118To130_Nominal/2018-11-21_DarkPhotonSR_mZ2-35_Norm/"
inputFileName           = "StatInput.root"
samples                 = [
                            "Higgs",
                            "qqZZ",
                            "ggZZ",
                            "HZZd_M7",
                            ]
prefix                  = "2e"
histName                = prefix+"-Norm"
rebinFactor             = 10

outputPath              = "/home/lucien/Higgs/DarkZ/DarkZ-StatFW/DataCard/2018-11-22_150p0_ParametricShape_v2/HZZd_M7/shape_"+prefix+".root"
drawDir                 = "/home/lucien/public_html/Higgs/DarkZ/StatFW/2018-11-22_Parametrization/"

# ___________________________________________________________________________________________ ||
fitter = ShapeFitter("massZ2",0.,1.)

def changeHist_ZX(hist):
    for ibin in range(1,hist.GetNbinsX()+1):
        binContent = hist.GetBinContent(ibin)
        binError = hist.GetBinContent(ibin)
        if ibin < 7 and binContent < 0.:
            hist.SetBinContent(ibin,1e-9)
        elif ibin >= 7 and binContent < 0.:
            hist.SetBinContent(ibin,-1*binContent)

sampleDict = {
        "Higgs":    Config(
                            rebinFactor=rebinFactor,
                            #pdfType="Hist",
                            #pdfInput=None,
                            pdfType="Poly",
                            pdfInput=[
                                    "Higgs",
                                    [
                                    ROOT.RooRealVar("c0_Higgs","c0_Higgs",  0.1,0.,5.),
                                    ROOT.RooRealVar("c1_Higgs","c1_Higgs",  0.,0.,2.),
                                    ROOT.RooRealVar("c2_Higgs","c2_Higgs",  0.,-5.,0.),
                                    ROOT.RooRealVar("c3_Higgs","c3_Higgs",  0.,-1.,1.),
                                    ROOT.RooRealVar("c4_Higgs","c4_Higgs",  0.,-1.,1.),
                                    ],
                                ],
                            histFunc=None,
                            ), 
        
        "HZZd_M7":  Config(
                            rebinFactor=1,
                            pdfType="BreitWigner",
                            pdfInput=["HZZd_M7","mean",0.,1.,"width",0.,300.],
                            histFunc=None,
                            ), 
 
        "qqZZ":     Config(
                            rebinFactor=rebinFactor,
                            #pdfType="Hist",
                            #pdfInput=None,
                            pdfType="Poly",
                            pdfInput=[
                                    "qqZZ",
                                    [
                                    ROOT.RooRealVar("c0_qqZZ","c0_qqZZ",  0.1,0.,5.),
                                    ROOT.RooRealVar("c1_qqZZ","c1_qqZZ",  0.,0.,2.),
                                    ROOT.RooRealVar("c2_qqZZ","c2_qqZZ",  0.,-5.,0.),
                                    ROOT.RooRealVar("c3_qqZZ","c3_qqZZ",  0.,-1.,1.),
                                    ROOT.RooRealVar("c4_qqZZ","c4_qqZZ",  0.,-1.,1.),
                                    ]
                                ],
                            histFunc=None,
                            ), 
        
        "ggZZ":     Config(
                            rebinFactor=rebinFactor,
                            #pdfType="Hist",
                            #pdfInput=None,
                            pdfType="Poly",
                            pdfInput=[
                                    "ggZZ",
                                    [
                                    ROOT.RooRealVar("c0_ggZZ","c0_ggZZ",  0.1,0.,5.),
                                    ROOT.RooRealVar("c1_ggZZ","c1_ggZZ",  0.,0.,2.),
                                    ROOT.RooRealVar("c2_ggZZ","c2_ggZZ",  0.,-5.,0.),
                                    ROOT.RooRealVar("c3_ggZZ","c3_ggZZ",  0.,-1.,1.),
                                    ROOT.RooRealVar("c4_ggZZ","c4_ggZZ",  0.,-1.,1.),
                                    ]
                                ],

                            histFunc=None,
                            ), 
        
        "ZPlusX":   Config(
                            rebinFactor=200,
                            pdfType="Landau",
                            pdfInput=[
                                #"Poly",
                                #[
                                #    ROOT.RooRealVar("c0_ZPlusX","c0_ZPlusX",  0.1,0.,5.),
                                #    ROOT.RooRealVar("c1_ZPlusX","c1_ZPlusX",  0.,-2.,2.),
                                #    ROOT.RooRealVar("c2_ZPlusX","c2_ZPlusX",  0.,-2.,2.),
                                #    ROOT.RooRealVar("c3_ZPlusX","c3_ZPlusX",  0.,-1.,1.),
                                #    ROOT.RooRealVar("c4_ZPlusX","c4_ZPlusX",  0.,-1.,1.),
                                #    ROOT.RooRealVar("c5_ZPlusX","c5_ZPlusX",  0.,-1.,1.),
                                #    ROOT.RooRealVar("c6_ZPlusX","c6_ZPlusX",  0.,-1.,1.),
                                #], 
                                "ZPlusX",
                                "meanVar_ZPlusX",
                                0.,
                                1.,
                                "widthVar_ZPlusX",
                                0.,
                                1.,
                                ],
                            histFunc=changeHist_ZX,
                            ),
        "Data2016": Config(
                            rebinFactor=rebinFactor,
                            pdfType="Data",
                            pdfInput=None,
                            histFunc=None,
                            ),
        }

outputFile = ROOT.TFile(outputPath,"RECREATE")
w = ROOT.RooWorkspace("parametric_pdf_"+prefix,"parametric_pdf_"+prefix)
c = ROOT.TCanvas("c1","c1",800,800)
c.cd()
for sample,config in sampleDict.iteritems():
    inputFile = ROOT.TFile(os.path.join(inputDir,sample,inputFileName),"READ")
    hist = inputFile.Get(histName)
    hist.Rebin(config.rebinFactor)
    if config.histFunc: config.histFunc(hist)
    if config.pdfType == pdfType_hist:
        #pdf,dataHist,argSet = fitter.makeRooHistPdf("Pdf_"+sample,hist)
        pdf,dataHist,argSet = fitter.makeRooHistPdf(sample,hist)
    elif config.pdfType == pdfType_data:
        pdf = ROOT.RooDataHist("data_obs","",ROOT.RooArgList(fitter.obsVar),hist)
    elif config.pdfType in [pdfType_BW,pdfType_poly,pdfType_landau]:
        if config.pdfType == pdfType_BW:
            pdf,meanVar,widthVar = fitter.makeBreitWignerPdf(*config.pdfInput)
        elif config.pdfType == pdfType_poly:
            pdf = fitter.makePolyPdf(*config.pdfInput)
        elif config.pdfType == pdfType_landau:
            pdf,meanVar,widthVar = fitter.makeLandauPdf(*config.pdfInput)
        config.evtYield = ROOT.RooRealVar("Yield","Yield", 0, 40)
        config.data = ROOT.RooDataHist("MCData_"+sample,"",ROOT.RooArgList(fitter.obsVar,config.evtYield),hist)
        result = pdf.fitTo(config.data)
        plot = fitter.obsVar.frame()
        config.data.plotOn(plot,ROOT.RooFit.Name("data"))
        pdf.plotOn(plot,ROOT.RooFit.Name("Parametric"))
        plot.Draw()
        c.SaveAs(drawDir+prefix+"_"+sample+".pdf")
    getattr(w,'import')(pdf)
    inputFile.Close()
outputFile.cd()
w.Write()
outputFile.Close()
