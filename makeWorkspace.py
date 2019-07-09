import glob,os,argparse

parser = argparse.ArgumentParser()
parser.add_argument("--inputDir",action="store")
parser.add_argument("--cardName",action="store",default="window.txt")
parser.add_argument("--combinePattern",action="store",default="")

option = parser.parse_args()

inputDir = option.inputDir

textFileName = os.path.join(inputDir,option.cardName)
print "*"*20
if option.combinePattern:
    print "Combining datacard with pattern in file name", option.combinePattern
    chStr = ""
    for each_ch_name in glob.glob(inputDir+option.combinePattern):
        chStr += " "+os.path.basename(each_ch_name).replace(".txt","")+"="+each_ch_name
    cmd = "combineCards.py "+chStr+" > "+textFileName
    print cmd
    os.system(cmd)
print "Making workspace from", textFileName
cmd = "text2workspace.py "+textFileName+" -v 1 --no-b-only"
print cmd
os.system(cmd)

