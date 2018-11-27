import ROOT,argparse

ROOT.gROOT.SetBatch(ROOT.kTRUE)

# ____________________________________________________________________________________ ||
parser = argparse.ArgumentParser()

parser.add_argument("--inputPath",action="store")
parser.add_argument("--outputPath",action="store")
parser.add_argument("--asimov",action="store_true")
parser.add_argument("--dir_name",action="store",default="shapes_prefit/TwoEl_SR")

bkg_names = [
        "ZPlusX",
        "ggZZ",
        "qqZZ",
        "Higgs",
        ]
stack_name = "bkg_stack"

color_dict = {
        "Higgs": ROOT.kAzure-2,
        "qqZZ": ROOT.kBlue+2,
        "ggZZ": ROOT.kBlue,
        "ZPlusX": ROOT.kViolet,
}

option = parser.parse_args()

dir_name = option.dir_name

# ____________________________________________________________________________________ ||
def tweak_hist(h,max=None,title=None):
    h.SetStats(0)
    if max: h.GetYaxis().SetRangeUser(0.,max)
    if not title:
        h.SetTitle("; m_{Z2} ;") 
    else:
        h.SetTitle(title)

# ____________________________________________________________________________________ ||
inputFile   = ROOT.TFile(option.inputPath,"READ")

tot_hist    = inputFile.Get(dir_name+"/total")
nbin        = tot_hist.GetNbinsX()
tot_hist.Scale(1./float(nbin))
maximum     = 1.2*tot_hist.GetMaximum()

tweak_hist(tot_hist,max=maximum)
tot_hist.SetLineStyle(9)
tot_hist.SetLineColor(ROOT.kRed)

bkg_stack    = ROOT.THStack(stack_name,stack_name)
for bkg_name in bkg_names:
    bkg_path = "/".join([dir_name,bkg_name])
    bkg_hist = inputFile.Get(bkg_path)
    bkg_hist.Scale(1./float(nbin))
    tweak_hist(bkg_hist,max=maximum)
    bkg_hist.SetFillColor(color_dict[bkg_name])
    bkg_stack.Add(bkg_hist)

bkg_err     = inputFile.Get(dir_name+"/total_background")
bkg_err.Scale(1./float(nbin))
for ibin in range(1,nbin+1): bkg_err.SetBinError(ibin,bkg_err.GetBinError(ibin)/float(nbin))
bkg_err.SetMarkerStyle(1)
bkg_err.SetLineColor(1)
bkg_err.SetLineWidth(3)
bkg_err.SetFillColor(13)
bkg_err.SetFillStyle(3001)

# ____________________________________________________________________________________ ||
c = ROOT.TCanvas()
tot_hist.Draw()
bkg_stack.Draw("same")
bkg_err.Draw("samee2")

c.SaveAs(option.outputPath)

# ____________________________________________________________________________________ ||
