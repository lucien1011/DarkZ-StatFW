import ROOT
import pprint
import sys

def getYield(h,mass,width,nbin=100):
    low_bin = h.GetXaxis().FindBin(mass*(1.-width))
    high_bin = h.GetXaxis().FindBin(mass*(1.+width))
    error = ROOT.Double(0.)
    integral = h.IntegralAndError(low_bin,high_bin,error)
    return integral/nbin,error/nbin


zd_mass_uncorr = float(sys.argv[1])
zd_mass = (zd_mass_uncorr-4.)/(35.-4.)

inputPath = "/home/lucien/Higgs/DarkZ/DarkZ-StatFW/DataCard/2018-11-28_150p0_ParametricShape_rebin_v10/HZZd_M%s/fitDiagnostics.root"%str(int(zd_mass_uncorr))
inputFile = ROOT.TFile(inputPath,"READ")

data_names = [
        "Data2016",
        ]

#bkg_names = mergeSampleDict.keys()
bkg_names = [
        "Higgs",
        "qqZZ",
        "ggZZ",
        "ZPlusX",
        "HZZd_M"+str(int(zd_mass_uncorr)),
        ]

dirName = "shapes_prefit/TwoEl_SR/"

printDict = {}

for bkg_name in bkg_names:
    h_el = inputFile.Get(dirName+bkg_name)
    h_mu = inputFile.Get(dirName.replace("El","Mu")+bkg_name)
    nbin = h_el.GetNbinsX()
    mu_count,mu_error = getYield(h_mu,zd_mass,0.02,nbin=nbin)
    el_count,el_error = getYield(h_el,zd_mass,0.05,nbin=nbin)
    printDict[bkg_name] = [mu_count,mu_error,el_count,el_error]

elOutStr = "rate\t\t"
muOutStr = ""
for name,l in printDict.iteritems():
    elOutStr += "%4.4f\t\t"%l[2]
    muOutStr += "%4.4f\t\t"%l[0]
print elOutStr+muOutStr
