import glob,os,argparse

parser = argparse.ArgumentParser()
parser.add_argument("--inputDir",action="store")
parser.add_argument("--option",action="store")

option = parser.parse_args()

inputDir = option.inputDir
pattern = "window_*.root"
method = "AsymptoticLimits"

for wsFileName in glob.glob(inputDir+pattern):
    print "*"*20
    print "Running on workspace", wsFileName
    items = ["combine","-M",method,wsFileName]
    if option.option: items += [option.option]
    cmd = " ".join(items)
    os.system(cmd)

