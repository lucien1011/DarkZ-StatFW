import os,copy,math,argparse,glob
from httplib import HTTPException

from Utilities.mkdir_p import mkdir_p

from CRABAPI.RawCommand import crabCommand
from CRABClient.ClientExceptions import CachefileNotFoundException,ConfigurationException
from CRABClient.UserUtilities import setConsoleLogLevel
from CRABClient.ClientUtilities import LOGLEVEL_MUTE

crab_resubmit_memory = 4000

parser = argparse.ArgumentParser()
#parser.add_argument("--inputDir",action="store")
parser.add_argument("--outputDir",action="store")
parser.add_argument("--pattern",action="store")
parser.add_argument("--dry_run",action="store_true")
parser.add_argument("--verbose",action="store_true")
parser.add_argument("--crab_stdout",action="store_true")
parser.add_argument("--purge",action="store_true")
parser.add_argument("--resubmit",action="store_true")
parser.add_argument("--inverse",action="store_true")

option = parser.parse_args()

if not option.crab_stdout:
    setConsoleLogLevel(LOGLEVEL_MUTE)

selectDir = glob.glob(option.pattern)
if option.inverse: selectDir = reversed(selectDir)
for crabDir in selectDir:
    if option.verbose:
        print "*"*100
        print "Running on directory "+crabDir
    try:
        status_cmd = 'status'
        status_res = crabCommand(status_cmd,dir=crabDir)
        print("Job status: "+status_res["dagStatus"])
    except HTTPException as ex:
        print("Problem with status encountered: %s" % ex)
    except CachefileNotFoundException as ex:
        print("Problem with status encountered: %s" % ex)

    if status_res["dagStatus"] == "COMPLETED" and option.purge:
        if option.verbose:
            print("Purging directory "+crabDir)
        try:
            purge_cmd = 'purge'
            res = crabCommand(purge_cmd,dir=crabDir)
        except HTTPException as ex:
            print("Problem with purge encountered: %s" % ex)
        except CachefileNotFoundException as ex:
            print("Problem with status encountered: %s" % ex) 
    elif status_res["dagStatus"] == "FAILED" and option.resubmit:
        if option.verbose:
            print("Resubmit directory "+crabDir)
        try:
            resubmit_cmd = 'resubmit'
            res = crabCommand(resubmit_cmd,dir=crabDir,maxmemory=str(crab_resubmit_memory))
        except HTTPException as ex:
            print("Problem with purge encountered: %s" % ex)
        except CachefileNotFoundException as ex:
            print("Problem with status encountered: %s" % ex) 
        except ConfigurationException as ex:
            print("Problem with status encountered: %s" % ex) 

    if option.verbose:
        print("*"*100)
