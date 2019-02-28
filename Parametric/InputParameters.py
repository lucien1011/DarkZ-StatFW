import os,ROOT
from ShapeFitConfig import ShapeFitConfig

ROOT.gROOT.SetBatch(ROOT.kTRUE)
ROOT.gSystem.Load("libHiggsAnalysisCombinedLimit.so")

# ___________________________________________________________________________________________ ||
rebinFactor             = 10

# ___________________________________________________________________________________________ ||
def changeHist_ZX(hist):
    for ibin in range(1,hist.GetNbinsX()+1):
        binContent = hist.GetBinContent(ibin)
        binError = hist.GetBinContent(ibin)
        if ibin < 7 and binContent < 0.:
            hist.SetBinContent(ibin,1e-9)
        elif ibin >= 7 and binContent < 0.:
            hist.SetBinContent(ibin,-1*binContent)

# ___________________________________________________________________________________________ ||
parameterDict = {
        "Higgs":    ShapeFitConfig(
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
        
        "HZZd_M4":  ShapeFitConfig(
                            rebinFactor=1,
                            #pdfType="BreitWigner",
                            #pdfInput=["HZZd_M4","mean",0.,1.,"width",0.,300.],
                            pdfType="DCB",
                            pdfInput=[
                                "HZZd_M4",
                                "mean",0.,1.,
                                "width",0.,300.,
                                "alphaL",0.1,50.,
                                "alphaR",0.1,50.,
                                "nL",0.1,50.,
                                "nR",0.1,50.,
                                ],
                            histFunc=None,
                            widthDict={
                                        "TwoMu_SR":0.02,
                                        "TwoEl_SR":0.05,
                                },
                            ),

        "HZZd_M7":  ShapeFitConfig(
                            rebinFactor=1,
                            #pdfType="BreitWigner",
                            #pdfInput=["HZZd_M7","mean",0.,1.,"width",0.,300.],
                            pdfType="DCB",
                            pdfInput=[
                                "HZZd_M7",
                                "mean",-1.,1.,
                                "width",0.00001,1.,
                                "alphaL",0.1,3.,
                                "alphaR",0.1,3.,
                                "nL",0.1,5.,
                                "nR",0.1,5.,
                                ],
                            histFunc=None,
                            widthDict={
                                        "TwoMu_SR":0.02/7.,
                                        "TwoEl_SR":0.05/7.,
                                },
                            ), 
        "HZZd_M10":  ShapeFitConfig(
                            rebinFactor=5,
                            #pdfType="BreitWigner",
                            #pdfInput=["HZZd_M10","mean",-1.,1.,"width",0.,300.],
                            pdfType="DCB",
                            pdfInput=[
                                "HZZd_M10",
                                "mean",0.,1.,
                                "width",0.0001,0.01,
                                "alphaL",0.1,3.,
                                "alphaR",0.1,3.,
                                "nL",0.1,5.,
                                "nR",0.1,5.,
                                ],
                            histFunc=None,
                            widthDict={
                                        "TwoMu_SR":0.02/10.,
                                        "TwoEl_SR":0.05/10.,
                                },                            
                            ), 
        "HZZd_M15":  ShapeFitConfig(
                            rebinFactor=1,
                            #pdfType="BreitWigner",
                            #pdfInput=["HZZd_M15","mean",-0.5,1.,"width",0.,300.],
                            pdfType="DCB",
                            pdfInput=[
                                "HZZd_M15",
                                "mean",0.,1.,
                                "width",0.0001,0.01,
                                "alphaL",0.1,3.,
                                "alphaR",0.1,3.,
                                "nL",0.1,5.,
                                "nR",0.1,5.,
                                ],
                            histFunc=None,
                            widthDict={
                                        "TwoMu_SR":0.02,
                                        "TwoEl_SR":0.05,
                                },
                            ), 
        "HZZd_M20":  ShapeFitConfig(
                            rebinFactor=1,
                            #pdfType="BreitWigner",
                            #pdfInput=["HZZd_M20","mean",0.,1.,"width",0.,300.],
                            pdfType="DCB",
                            pdfInput=[
                                "HZZd_M20",
                                "mean",0.,1.,
                                "width",0.0001,0.01,
                                "alphaL",0.1,3.,
                                "alphaR",0.1,3.,
                                "nL",0.1,5.,
                                "nR",0.1,5.,
                                ],
                                                  
                            histFunc=None,
                            widthDict={
                                        "TwoMu_SR":0.02,
                                        "TwoEl_SR":0.05,
                                },
                            ), 
        "HZZd_M25":  ShapeFitConfig(
                            rebinFactor=1,
                            #pdfType="BreitWigner",
                            #pdfInput=["HZZd_M25","mean",0.,1.,"width",0.,300.],
                            pdfType="DCB",
                            pdfInput=[
                                "HZZd_M25",
                                "mean",0.,1.,
                                "width",0.0001,0.01,
                                "alphaL",0.1,3.,
                                "alphaR",0.1,3.,
                                "nL",0.1,5.,
                                "nR",0.1,5.,
                                ],
                            histFunc=None,
                            widthDict={
                                        "TwoMu_SR":0.02,
                                        "TwoEl_SR":0.05,
                                },
                            ), 
        "HZZd_M30":  ShapeFitConfig(
                            rebinFactor=1,
                            #pdfType="BreitWigner",
                            #pdfInput=["HZZd_M30","mean",0.,5.,"width",0.,300.],
                            pdfType="DCB",
                            pdfInput=[
                                "HZZd_M30",
                                "mean",0.,1.,
                                "width",0.0001,0.01,
                                "alphaL",0.1,3.,
                                "alphaR",0.1,3.,
                                "nL",0.1,5.,
                                "nR",0.1,5.,
                                ],

                            histFunc=None,
                            widthDict={
                                        "TwoMu_SR":0.02,
                                        "TwoEl_SR":0.05,
                                },
                            ), 
         
         "qqZZ":     ShapeFitConfig(
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
        
        "ggZZ":     ShapeFitConfig(
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
        
        "ZPlusX":   ShapeFitConfig(
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
        "Data2016": ShapeFitConfig(
                            rebinFactor=1,
                            pdfType="Data",
                            pdfInput=None,
                            histFunc=None,
                            ),
        }
