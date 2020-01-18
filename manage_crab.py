import os,copy,math,argparse,glob
from Utilities.mkdir_p import mkdir_p
from CRABAPI.RawCommand import crabCommand
from CRABClient.ClientExceptions import CachefileNotFoundException
from httplib import HTTPException

parser = argparse.ArgumentParser()
#parser.add_argument("--inputDir",action="store")
parser.add_argument("--outputDir",action="store")
parser.add_argument("--pattern",action="store")
parser.add_argument("--dry_run",action="store_true")
parser.add_argument("--verbose",action="store_true")
parser.add_argument("--purge",action="store_true")


option = parser.parse_args()

for crabDir in glob.glob(option.pattern):
    if option.verbose:
        print "*"*100
        print "Running on directory "+crabDir
    try:
        status_res = crabCommand('status',dir=crabDir)
    except HTTPException as ex:
        print("Problem with status encountered: %s" % ex)
    except CachefileNotFoundException as ex:
        print("Problem with status encountered: %s" % ex)

    if status_res["dagStatus"] == "COMPLETED" and option.purge:
        if option.verbose:
            print "Purging directory "+crabDir
        try:
            res = crabCommand('purge',dir=crabDir)
        except HTTPException as ex:
            print("Problem with purge encountered: %s" % ex)
        except CachefileNotFoundException as ex:
            print("Problem with status encountered: %s" % ex) 

    if option.verbose:
        print "*"*100
