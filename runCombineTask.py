import glob,os,argparse,subprocess
from CombineAPI.CombineInterface import CombineAPI,CombineOption 
from Parametric.InputParameters import parameterDict
from BatchWorker.CrabWorker import CrabWorker,CrabConfig

parser = argparse.ArgumentParser()
parser.add_argument("--inputDir",action="store")
parser.add_argument("--selectStr",action="store")
parser.add_argument("--option",action="store",default="",type=str)
parser.add_argument("--pattern",action="store")
parser.add_argument("--method",action="store",default="AsymptoticLimits")
parser.add_argument("--crab",action="store_true")
parser.add_argument("--taskName",action="store",default="test")
parser.add_argument("--dry_run",action="store_true")
parser.add_argument("--run_in_wsdir",action="store_true")
parser.add_argument("--tag",action="store")

option = parser.parse_args()

inputDir = option.inputDir
pattern = "window*.root" if not option.pattern else option.pattern

shell_script_template = """
#!/bin/sh
set -x
set -e
ulimit -s unlimited
ulimit -c 0
function error_exit
{
  if [ $1 -ne 0 ]; then
    echo "Error with exit code ${1}"
    if [ -e FrameworkJobReport.xml ]
    then
      cat << EOF > FrameworkJobReport.xml.tmp
      <FrameworkJobReport>
      <FrameworkError ExitStatus="${1}" Type="" >
      Error with exit code ${1}
      </FrameworkError>
EOF
      tail -n+2 FrameworkJobReport.xml >> FrameworkJobReport.xml.tmp
      mv FrameworkJobReport.xml.tmp FrameworkJobReport.xml
    else
      cat << EOF > FrameworkJobReport.xml
      <FrameworkJobReport>
      <FrameworkError ExitStatus="${1}" Type="" >
      Error with exit code ${1}
      </FrameworkError>
      </FrameworkJobReport>
EOF
    fi
    exit 0
  fi
}
trap 'error_exit $?' ERR

ls -lrt
%s >> combine_log.txt

tar -cf combine_output.tar *.root
rm higgsCombine*.root
"""

api = CombineAPI()
for cardDir in glob.glob(inputDir+"*"+option.selectStr+"*/"):
    print "********************"
    print "Running on directory "+cardDir
    if not option.crab:
        wsFilePath = os.path.abspath(cardDir+cardDir.split("/")[-2]+".root")
        optionList = option.option.split()
        combineOption = CombineOption(os.path.abspath(cardDir),wsFilePath,option=optionList,verbose=True,method=option.method,run_in_wsdir=option.run_in_wsdir,tag=option.tag)
        api.run(combineOption)
    else:
        pwdPath = os.environ['PWD']
        wsFilePath = cardDir+cardDir.split("/")[-2]+".root"
        optionList = option.option.split()
        combineOption = CombineOption(cardDir,os.path.basename(wsFilePath),option=optionList,verbose=True,method=option.method)
        combine_cmd = api.make_cmd(combineOption)
        worker = CrabWorker()
        crabConfig = CrabConfig(
                "CrabConfig",
                crab_file_path = os.path.join(cardDir,"combine_crab.py"),
                taskName = option.taskName,
                JobType_plugName = 'PrivateMC',
                JobType_psetName = 'os.environ[\'CMSSW_BASE\']+\'/src/CombineHarvester/CombineTools/scripts/do_nothing_cfg.py\'',
                JobType_scriptExe = 'combine_crab.sh',
                JobType_inputFiles = '[os.environ[\'CMSSW_BASE\']+\'/src/CombineHarvester/CombineTools/scripts/FrameworkJobReport.xml\', os.environ[\'CMSSW_BASE\']+\'/src/CombineHarvester/CombineTools/scripts/copyRemoteWorkspace.sh\', os.environ[\'CMSSW_BASE\']+\'/bin/\'+os.environ[\'SCRAM_ARCH\']+\'/combine\',\'{wsFileName}\']'.format(wsFileName=os.path.abspath(wsFilePath)),
                JobType_outputFiles = '[\'combine_output.tar\',\'combine_log.txt\',]',
                Data_outputPrimaryDataset = 'Combine',
                Data_unitsPerJob = 1,
                Data_totalUnits = 1,
                Data_publication = False,
                Data_outputDatasetTag = '',
                Data_outLFNDirBase = '\'/store/user/%s/HiggsCombine/\' % (getUsernameFromSiteDB()) + taskName + \'/{modelName}/\''.format(modelName=cardDir.split("/")[-2],),
                Site_storageSite = 'T2_US_Florida',
                )
        execConfig = CrabConfig(
                "ExecConfig",
                exec_file_path = os.path.join(cardDir,"combine_crab.sh"),
                cmd_str = shell_script_template%("./"+combine_cmd),
                )
        worker.make_exec_file(execConfig)
        worker.make_crab_file(crabConfig)
        if not option.dry_run:
            os.chdir(cardDir)
            #worker.submit(os.path.abspath(os.path.join(cardDir,"combine_condor.job")))
            worker.submit("combine_crab.py")
            os.chdir(pwdPath)
