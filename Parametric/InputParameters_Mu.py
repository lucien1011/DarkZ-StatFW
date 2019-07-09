import os,ROOT
from ShapeFitConfig import ShapeFitConfig

ROOT.gROOT.SetBatch(ROOT.kTRUE)
ROOT.gSystem.Load("libHiggsAnalysisCombinedLimit.so")

# ___________________________________________________________________________________________ ||
rebinFactor             = 10
postfix                 = "_Mu"

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
parameterDict_Mu = {
        "Higgs":    ShapeFitConfig(
                            rebinFactor=rebinFactor,
                            #pdfType="Hist",
                            #pdfInput=None,
                            pdfType="Poly",
                            pdfInput=[
                                    "Higgs",
                                    [
                                    ROOT.RooRealVar("c0_Higgs"+postfix,"c0_Higgs"+postfix,  0.1,0.,5.),
                                    ROOT.RooRealVar("c1_Higgs"+postfix,"c1_Higgs"+postfix,  0.,0.,2.),
                                    ROOT.RooRealVar("c2_Higgs"+postfix,"c2_Higgs"+postfix,  0.,-5.,0.),
                                    ROOT.RooRealVar("c3_Higgs"+postfix,"c3_Higgs"+postfix,  0.,-1.,1.),
                                    ROOT.RooRealVar("c4_Higgs"+postfix,"c4_Higgs"+postfix,  0.,-1.,1.),
                                    ],
                                ],
                            histFunc=None,
                            ), 
        
        "HZZd_M4":  ShapeFitConfig(
                            rebinFactor=5,
                            #pdfType="BreitWigner",
                            #pdfInput=[
                            #    "HZZd_M4",
                            #    "mean"+postfix,
                            #    0.,1.,
                            #    "width"+postfix,0.,300.
                            #    ],
                            pdfType="DCB",
                            pdfInput=[
                                "HZZd_M4",
                                "mean"+postfix,-2.,2.,
                                "width"+postfix,0.00001,1.,
                                "alphaL"+postfix,0.01,3.,
                                "alphaR"+postfix,0.01,3.,
                                "nL"+postfix,0.01,5.,
                                "nR"+postfix,0.01,5.,
                                ],
                            histFunc=None,
                            widthDict={
                                        "TwoMu_SR":0.02/4.,
                                        "TwoEl_SR":0.05/4.,
                                },
                            ),

        "HZZd_M7":  ShapeFitConfig(
                            rebinFactor=1,
                            #pdfType="BreitWigner",
                            #pdfInput=[
                            #    "HZZd_M7",
                            #    "mean"+postfix,
                            #    0.,1.,
                            #    "width"+postfix,0.,300.
                            #    ],
                            pdfType="DCB",
                            pdfInput=[
                                "HZZd_M7",
                                "mean"+postfix,-1.,1.,
                                "width"+postfix,0.000001,1.,
                                "alphaL"+postfix,0.1,3.,
                                "alphaR"+postfix,0.1,3.,
                                "nL"+postfix,0.1,5.,
                                "nR"+postfix,0.1,5.,
                                ],
                            histFunc=None,
                            widthDict={
                                        "TwoMu_SR":0.02/7.,
                                        "TwoEl_SR":0.05/7.,
                                },
                            ), 
        "HZZd_M10":  ShapeFitConfig(
                            rebinFactor=2,
                            #pdfType="BreitWigner",
                            #pdfInput=[
                            #    "HZZd_M10",
                            #    "mean"+postfix,
                            #    0.,1.,
                            #    "width"+postfix,0.,300.
                            #    ],
                            pdfType="DCB",
                            pdfInput=[
                                "HZZd_M10",
                                "mean"+postfix,0.,1.,
                                "width"+postfix,0.00001,1,
                                "alphaL"+postfix,0.1,3.,
                                "alphaR"+postfix,0.1,3.,
                                "nL"+postfix,0.1,5.,
                                "nR"+postfix,0.1,5.,
                                ],
                            histFunc=None,
                            widthDict={
                                        "TwoMu_SR":0.02/10.,
                                        "TwoEl_SR":0.05/10.,
                                },                            
                            ), 
        "HZZd_M15":  ShapeFitConfig(
                            rebinFactor=2,
                            #pdfType="BreitWigner",
                            #pdfInput=[
                            #    "HZZd_M15",
                            #    "mean"+postfix,
                            #    0.,1.,
                            #    "width"+postfix,0.,300.
                            #    ],
                            pdfType="DCB",
                            pdfInput=[
                                "HZZd_M15",
                                "mean"+postfix,0.,1.,
                                "width"+postfix,0.00001,0.01,
                                "alphaL"+postfix,0.1,3.,
                                "alphaR"+postfix,0.1,3.,
                                "nL"+postfix,0.1,5.,
                                "nR"+postfix,0.1,5.,
                                ],
                            histFunc=None,
                            widthDict={
                                        "TwoMu_SR":0.02/15.,
                                        "TwoEl_SR":0.05/15.,
                                },
                            ), 
        "HZZd_M20":  ShapeFitConfig(
                            rebinFactor=5,
                            #pdfType="BreitWigner",
                            #pdfInput=[
                            #    "HZZd_M20",
                            #    "mean"+postfix,
                            #    0.,1.,
                            #    "width"+postfix,0.,300.
                            #    ],
                            pdfType="DCB",
                            pdfInput=[
                                "HZZd_M20",
                                "mean"+postfix,0.,1.,
                                "width"+postfix,0.0001,0.01,
                                "alphaL"+postfix,0.1,3.,
                                "alphaR"+postfix,0.1,3.,
                                "nL"+postfix,0.1,5.,
                                "nR"+postfix,0.1,5.,
                                ],
                            histFunc=None,
                            widthDict={
                                        "TwoMu_SR":0.02/20.,
                                        "TwoEl_SR":0.05/20.,
                                },
                            ), 
        "HZZd_M25":  ShapeFitConfig(
                            rebinFactor=5,
                            #pdfType="BreitWigner",
                            #pdfInput=[
                            #    "HZZd_M25",
                            #    "mean"+postfix,
                            #    0.,1.,
                            #    "width"+postfix,0.,300.
                            #    ],
                            pdfType="DCB",
                            pdfInput=[
                                "HZZd_M25",
                                "mean"+postfix,0.,1.,
                                "width"+postfix,0.0001,0.01,
                                "alphaL"+postfix,0.1,3.,
                                "alphaR"+postfix,0.1,3.,
                                "nL"+postfix,0.1,5.,
                                "nR"+postfix,0.1,5.,
                                ],
                            histFunc=None,
                            widthDict={
                                        "TwoMu_SR":0.02/25.,
                                        "TwoEl_SR":0.05/25.,
                                },
                            ), 
        "HZZd_M30":  ShapeFitConfig(
                            rebinFactor=5,
                            #pdfType="BreitWigner",
                            #pdfInput=[
                            #    "HZZd_M30",
                            #    "mean"+postfix,
                            #    0.,1.,
                            #    "width"+postfix,0.,300.
                            #    ],
                            pdfType="DCB",
                            pdfInput=[
                                "HZZd_M30",
                                "mean"+postfix,0.,1.,
                                "width"+postfix,0.0001,0.01,
                                "alphaL"+postfix,0.1,3.,
                                "alphaR"+postfix,0.1,3.,
                                "nL"+postfix,0.1,5.,
                                "nR"+postfix,0.1,5.,
                                ],
                            histFunc=None,
                            widthDict={
                                        "TwoMu_SR":0.02/30.,
                                        "TwoEl_SR":0.05/30.,
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
                                    ROOT.RooRealVar("c0_qqZZ"+postfix,"c0_qqZZ"+postfix,  0.1,0.,5.),
                                    ROOT.RooRealVar("c1_qqZZ"+postfix,"c1_qqZZ"+postfix,  0.,0.,2.),
                                    ROOT.RooRealVar("c2_qqZZ"+postfix,"c2_qqZZ"+postfix,  0.,-5.,0.),
                                    ROOT.RooRealVar("c3_qqZZ"+postfix,"c3_qqZZ"+postfix,  0.,-1.,1.),
                                    ROOT.RooRealVar("c4_qqZZ"+postfix,"c4_qqZZ"+postfix,  0.,-1.,1.),
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
                                    ROOT.RooRealVar("c0_ggZZ"+postfix,"c0_ggZZ"+postfix,  0.1,0.,5.),
                                    ROOT.RooRealVar("c1_ggZZ"+postfix,"c1_ggZZ"+postfix,  0.,0.,2.),
                                    ROOT.RooRealVar("c2_ggZZ"+postfix,"c2_ggZZ"+postfix,  0.,-5.,0.),
                                    ROOT.RooRealVar("c3_ggZZ"+postfix,"c3_ggZZ"+postfix,  0.,-1.,1.),
                                    ROOT.RooRealVar("c4_ggZZ"+postfix,"c4_ggZZ"+postfix,  0.,-1.,1.),
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
                                "meanVar_ZPlusX"+postfix,
                                0.,
                                1.,
                                "widthVar_ZPlusX"+postfix,
                                0.,
                                1.,
                                ],
                            histFunc=changeHist_ZX,
                            ),
        #"Data2016": ShapeFitConfig(
        "Data": ShapeFitConfig(
                            rebinFactor=10,
                            pdfType="Data",
                            pdfInput=None,
                            histFunc=None,
                            ),
        }
