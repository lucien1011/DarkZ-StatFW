import glob,os,argparse

parser = argparse.ArgumentParser()
parser.add_argument("--inputDir",action="store")

option = parser.parse_args()

inputDir = option.inputDir
pattern = "window_*.txt"

for textFileName in glob.glob(inputDir+pattern):
    print "*"*20
    print "Making workspace from", textFileName
    cmd = "text2workspace.py "+textFileName
    os.system(cmd)

