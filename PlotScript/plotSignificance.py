import ROOT,glob,os,argparse,operator
from collections import OrderedDict

ROOT.gROOT.SetBatch(ROOT.kTRUE)

parser = argparse.ArgumentParser()
parser.add_argument("--inputDir",action="store")
parser.add_argument("--outputPath",action="store")
parser.add_argument("--selectStr",action="store",default="")

option = parser.parse_args()

inputDir = option.inputDir

#quantiles       = ["down2","down1","central","up1","up2","obs"]
quantiles       = ["obs",]
varName         = "limit"

# ________________________________________________________________ ||
# Read limit from directory
# ________________________________________________________________ ||
outDict = OrderedDict()
for quantile in quantiles:
    outDict[quantile] = OrderedDict()
for cardDir in glob.glob(inputDir+"*"+option.selectStr+"*/"):
    print "Reading directory "+cardDir
    inputFile = ROOT.TFile(cardDir+"higgsCombineTest.Significance.mH120.root","READ")
    tree = inputFile.Get("limit")
    window_name = cardDir.split("/")[-2]
    window_value = float(window_name.split("_")[1].replace("MZD",""))
    for i,entry in enumerate(tree):
        outDict[quantiles[i]][window_value] = getattr(entry,varName)
for quantile in quantiles:
    print max(outDict[quantile].iteritems(), key=operator.itemgetter(1))
