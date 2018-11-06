from Core.BaseDataset import BaseDataset

# ____________________________________________________________________________________________________________________________________________ ||
# Z+X
ZPlusX = BaseDataset(
        "ZPlusX",
        isMC                = True,
        )

# ____________________________________________________________________________________________________________________________________________ ||
# Data2016
data2016 = BaseDataset(
        "Data2016",
        isMC                = False,
        )

# ____________________________________________________________________________________________________________________________________________ ||
# ggZZTo4tau
ggZZTo4tau = BaseDataset(
        "ggZZTo4tau",
        isMC                = True,
        #xs                  = 0.001586,
        )

# ____________________________________________________________________________________________________________________________________________ ||
# ggZZTo4e
ggZZTo4e = BaseDataset(
        "ggZZTo4e",
        isMC                = True,
        #xs                  = 0.001586,
        )

# ____________________________________________________________________________________________________________________________________________ ||
# ggZZTo4mu
ggZZTo4mu = BaseDataset(
        "ggZZTo4mu",
        isMC                = True,
        #xs                  = 0.001586,
        )

# ____________________________________________________________________________________________________________________________________________ ||
# ggZZTo2mu2tau
ggZZTo2mu2tau = BaseDataset(
        "ggZZTo2mu2tau",
        #xs                  = 0.00319,
        )

# ____________________________________________________________________________________________________________________________________________ ||
# ggZZTo2e2mu
ggZZTo2e2mu = BaseDataset(
        "ggZZTo2e2mu",
        isMC                = True,
        #xs                  = 0.00319,
        )

# ____________________________________________________________________________________________________________________________________________ ||
# ggZZTo2e2tau
ggZZTo2e2tau = BaseDataset(
        "ggZZTo2e2tau",
        isMC                = True,
        #xs                  = 0.00319,
        )

# ____________________________________________________________________________________________________________________________________________ ||
# qqZZ
qqZZTo4L = BaseDataset(
        "qqZZTo4L",
        isMC                = True,
        #xs                  = 1.256,
        )

# ____________________________________________________________________________________________________________________________________________ ||
# ggH
ggH = BaseDataset(
        "ggH",
        isMC                = True,
        #xs                  = 0.01218,
        #xs                  = 48.52*0.0002768,
        )

# ____________________________________________________________________________________________________________________________________________ ||
# VBF
VBF = BaseDataset(
        "VBF",
        isMC                = True,
        #xs                  = 0.001044,
        )

# ____________________________________________________________________________________________________________________________________________ ||
# WHplus
WHplus = BaseDataset(
        "WHplus",
        isMC                = True,
        #xs                  = 0.000232,
        )

# ____________________________________________________________________________________________________________________________________________ ||
# WHminus
WHminus = BaseDataset(
        "WHminus",
        isMC                = True,
        #xs                  = 0.000147,
        )

# ____________________________________________________________________________________________________________________________________________ ||
# ZH
ZH = BaseDataset(
        "ZH",
        isMC                = True,
        #xs                  = 0.000668,
        )

# ____________________________________________________________________________________________________________________________________________ ||
# ggHZZd_M15
ggHZZd_M15 = BaseDataset(
        "HZZd_M15",
        isMC                = True,
        isSignal            = True,
        #xs                  = 0.0000119*100,
        #xs                  = 48.58*0.001,
        )

# ____________________________________________________________________________________________________________________________________________ ||
# ggHZZd_M20
ggHZZd_M20 = BaseDataset(
        "HZZd_M20",
        isMC                = True,
        isSignal            = True,
        #xs                  = 6.285e-06*100,
        #xs                  = 48.58*0.001,
        )

# ____________________________________________________________________________________________________________________________________________ ||
# ggHZZd_M25
ggHZZd_M25 = BaseDataset(
        "HZZd_M25",
        isMC                = True,
        isSignal            = True,
        #xs                  = 9.857e-06*100,
        #xs                  = 48.58*0.001,
        )

# ____________________________________________________________________________________________________________________________________________ ||
# ggHZZd_M30
ggHZZd_M30 = BaseDataset(
        "HZZd_M30",
        isMC                = True,
        isSignal            = True,
        #xs                  = 1.190e-05*100,
        #xs                  = 48.58*0.001,
        )

# ____________________________________________________________________________________________________________________________________________ ||
# ggHZZd_M4
ggHZZd_M4 = BaseDataset(
        "HZZd_M4",
        isMC                = True,
        isSignal            = True,
        #xs                  = 1.190e-05*100,
        #xs                  = 48.58*0.001,
        )

# ____________________________________________________________________________________________________________________________________________ ||
# ggHZZd_M7
ggHZZd_M7 = BaseDataset(
        "HZZd_M7",
        isMC                = True,
        isSignal            = True,
        #xs                  = 1.190e-05*100,
        #xs                  = 48.58*0.001,
        )

# ____________________________________________________________________________________________________________________________________________ ||
# ggHZZd_M10
ggHZZd_M10 = BaseDataset(
        "HZZd_M10",
        isMC                = True,
        isSignal            = True,
        #xs                  = 1.190e-05*100,
        #xs                  = 48.58*0.001,
        )

# ____________________________________________________________________________________________________________________________________________ ||
## ggHZZd_M35
#ggHZZd_M35_cmpList = ComponentList(
#        [ Component("ggHZZd_M35",sigSkimTreeDir+"ZD_UpTo0j_MZD35_Eps1e-2_klo.root","passedEvents",inUFTier2=inUFTier2) ]
#        )
#ggHZZd_M35 = BaseDataset(
#        "ggHZZd_M35",
#        ggHZZd_M35_cmpList,
#        isMC                = True,
#        isSignal            = True,
#        xs                  = 6.285e-06*100,
#        #xs                  = 48.58*0.001,
#        )
#ggHZZd_M35.setSumWeight(sigTreeDir+"ZD_UpTo0j_MZD35_Eps1e-2_klo.root","Ana/sumWeights",False)


# ____________________________________________________________________________________________________________________________________________ ||
bkgSamples = [
        ggH,
        VBF,
        WHplus,
        WHminus,
        ZH,
        qqZZTo4L,
        ggZZTo2e2mu,
        ggZZTo2e2tau,
        ggZZTo2mu2tau,
        ggZZTo4e,
        ggZZTo4mu,
        ggZZTo4tau,
        ZPlusX,
        #data2016,
        ]

sigSamples = [
        ggHZZd_M4,
        ggHZZd_M7,
        ggHZZd_M10,
        ggHZZd_M15,
        ggHZZd_M20,
        ggHZZd_M25,
        ggHZZd_M30,
        #ggHZZd_M35,
        ]

componentList = bkgSamples + sigSamples + [data2016]
