import os,copy,math,argparse,glob,shutil
from Utilities.mkdir_p import mkdir_p

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
        print "Copying "+fpath
        print "Output directory: "+outputDir
    mkdir_p(outputDir)
    if not option.dry_run:
        shutil.copyfile(fpath,os.path.join(outputDir,os.path.basename(fpath)))
if option.verbose:
    print "\n"*1
print "*"*40
print "Summary"
print "*"*40
print "Copied files: ",len(glob.glob(option.pattern))
