import glob,os,argparse,subprocess
from CombineAPI.CombineInterface import CombineAPI,CombineOption 
from Parametric.InputParameters import parameterDict

parser = argparse.ArgumentParser()
parser.add_argument("--inputDir",action="store")
parser.add_argument("--selectStr",action="store")
parser.add_argument("--option",action="store",default=str)
parser.add_argument("--pattern",action="store")
parser.add_argument("--method",action="store",default="AsymptoticLimits")

option = parser.parse_args()

inputDir = option.inputDir
pattern = "window*.root" if not option.pattern else option.pattern

api = CombineAPI()
for cardDir in glob.glob(inputDir+"*"+option.selectStr+"*/"):
    print "Running on directory "+cardDir
    wsFilePath = cardDir+cardDir.split("/")[-2]+".root"
    optionList = option.option.split()
    combineOption = CombineOption(cardDir,wsFilePath,option=optionList,verbose=True,method=option.method)
    api.run(combineOption)
