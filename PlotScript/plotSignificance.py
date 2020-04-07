import ROOT,glob,os,argparse,operator
from collections import OrderedDict
from StatFW.BaseObject import BaseObject

ROOT.gROOT.SetBatch(ROOT.kTRUE)

parser = argparse.ArgumentParser()
parser.add_argument("--inputDir",action="store")
parser.add_argument("--outputPath",action="store")
parser.add_argument("--selectStr",action="store",default="")

option = parser.parse_args()

inputDir = option.inputDir

quantiles       = [
    BaseObject("central",
        asymp_file_name="higgsCombineTest.Significance.mH120.expected.root",
        entry = 0,
        #hybridnew_file_name="higgsCombineTest.HybridNew.mH120.quant0.500.root",
        ),
    BaseObject("obs",
        asymp_file_name="higgsCombineTest.Significance.mH120.observed.root",
        entry = 0,
        #asymp_file_name="higgsCombineTest.Significance.mH120.root",
        #hybridnew_file_name="higgsCombineTest.HybridNew.mH120.root",
        ),
    ]
varName         = "limit"

# ________________________________________________________________ ||
# Read limit from directory
# ________________________________________________________________ ||
outDict = OrderedDict()
for quantile in quantiles:
    outDict[quantile] = OrderedDict()
for cardDir in glob.glob(inputDir+"*"+option.selectStr+"*/"):
    print "Reading directory "+cardDir
    window_name = cardDir.split("/")[-2]
    window_value = float(window_name.split("_")[1].replace("MZD",""))
    for i,quan in enumerate(quantiles):
        inputFile = ROOT.TFile(cardDir+quan.asymp_file_name,"READ")
        tree = inputFile.Get(varName)
        tree.GetEntry(quan.entry)
        outDict[quan][window_value] = getattr(tree,varName)
        inputFile.Close()
        print quan.name,outDict[quan][window_value]
for quantile in quantiles:
    print "-"*100
    print quantile.name
    print "Maximum local significance: ",max(outDict[quantile].iteritems(), key=operator.itemgetter(1))
    print "Proportion of 2sigma significance: ",sum([1. for window_value,sigma in outDict[quantile].iteritems() if sigma > 2.])/len(outDict[quantile])


