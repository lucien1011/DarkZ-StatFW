import glob,os,argparse,subprocess
from CombineAPI.CombineInterface import CombineAPI,CombineOption 

parser = argparse.ArgumentParser()
parser.add_argument("--inputDir",action="store")
parser.add_argument("--selectStr",action="store")
parser.add_argument("--option",action="store")

option = parser.parse_args()

inputDir = option.inputDir
pattern = "window*.root"
method = "AsymptoticLimits"

api = CombineAPI()
for cardDir in glob.glob(inputDir+"*"+option.selectStr+"*/"):
    print "Running on directory "+cardDir
    wsFilePath = cardDir+cardDir.split("/")[-2]+".root"
    combineOption = CombineOption(cardDir,wsFilePath,option=option.option)
    api.run(combineOption)
