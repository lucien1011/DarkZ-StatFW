import os,copy,math,argparse,glob,tarfile
from Utils.mkdir_p import mkdir_p

parser = argparse.ArgumentParser()
#parser.add_argument("--inputDir",action="store")
parser.add_argument("--outputDir",action="store")
parser.add_argument("--pattern",action="store")
parser.add_argument("--dry_run",action="store_true")
parser.add_argument("--verbose",action="store_true")

option = parser.parse_args()

nExistDir = 0
for fpath in glob.glob(option.pattern):
    outputDir = os.path.join(option.outputDir,fpath.split("/")[8]+"/")
    if option.verbose:
        print "*"*40
        print "Untarring "+fpath
        print "Output directory: "+outputDir
    if os.path.exists(os.path.join(outputDir,"higgsCombineTest.HybridNew.mH120.root")): nExistDir += 1
    mkdir_p(outputDir)
    if not option.dry_run:
        my_tar = tarfile.open(fpath)
        my_tar.extractall(outputDir) # specify which folder to extract to
        my_tar.close()
if option.verbose:
    print "\n"*1
print "*"*40
print "Summary"
print "*"*40
print "Available tar files: ",len(glob.glob(option.pattern))
print "Possible tarred files: ",nExistDir
