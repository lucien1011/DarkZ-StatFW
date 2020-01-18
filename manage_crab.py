import os,copy,math,argparse,glob
from Utilities.mkdir_p import mkdir_p
from CRABAPI.RawCommand import crabCommand

parser = argparse.ArgumentParser()
#parser.add_argument("--inputDir",action="store")
parser.add_argument("--outputDir",action="store")
parser.add_argument("--pattern",action="store")
parser.add_argument("--dry_run",action="store_true")
parser.add_argument("--verbose",action="store_true")

option = parser.parse_args()

for crabDir in glob.glob(option.pattern):
    if option.verbose:
        print "********************"
        print "Running on directory "+crabDir
    res = crabCommand('status',dir=crabDir)
