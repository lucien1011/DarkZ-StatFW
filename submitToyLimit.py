import glob,os,argparse,subprocess
from CombineAPI.CombineInterface import CombineAPI,CombineOption 
from Parametric.InputParameters import parameterDict
from BatchWorker.CrabWorker import CrabWorker,CrabConfig
from Utilities.mkdir_p import mkdir_p

# ____________________________________________________________________________________________________________________________________________ ||
#inputDir        = "/cms/data/store/user/klo/HiggsCombineWorkspace/HIG-19-007/XX_2020-03-03_SR2D_RunII/"
#taskName        = "2020-03-06_SR2D_RunII"

inputDir        = "/cms/data/store/user/klo/HiggsCombineWorkspace/HIG-19-007/XX_2020-03-17_SR2D_RunII/"
taskName        = "2020-03-17_SR2D_RunII"

# ____________________________________________________________________________________________________________________________________________ ||
#mass_points     = [4,5,6,7,8,9,10,15,20,25,30,35,40,45,50,55,60]
mass_points     = [4.20*1.005**i for i in range(541)]
crabTaskDir     = "crabTaskDir/"
dry_run         = False
method          = "HybridNew"
option          = ""
crabUserName    = "klo"

# ____________________________________________________________________________________________________________________________________________ ||
shell_script_template = """
#!/bin/sh
#set -x
#set -e
#ulimit -s unlimited
#ulimit -c 0
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
%s
ls -lrt

tar -cf combine_output.tar *.root
rm higgsCombine*.root
"""

api = CombineAPI()
for m in mass_points:
    print "*"*100
    print "Running on mass point "+str(m)
    modelName = "Zd_MZD"+str(m)
    crabDir = os.path.join(crabTaskDir,taskName,modelName)
    mkdir_p(crabDir)
    pwdPath = os.environ['PWD']
    wsFilePath = os.path.join(inputDir,modelName,modelName+".root")
    optionList = option.split()
    combine_cmd_list = []
    wsFilePathRoot = wsFilePath.replace("/cms/data","root://cms-xrd-global.cern.ch/")
    combine_cmd_list.append('./copyRemoteWorkspace.sh %s ./%s ' % (wsFilePathRoot, os.path.basename(wsFilePathRoot)))
    combineOption = CombineOption(crabDir,os.path.basename(wsFilePath),option=optionList,verbose=True,method=method)
    combine_cmd_list.append("./"+api.make_cmd(combineOption)+" >> combine_log.txt")
    for quantile in [0.500,0.840,0.160,0.975,0.025]:
        combineOption = CombineOption(crabDir,os.path.basename(wsFilePath),option=optionList+["--expectedFromGrid="+str(quantile)],verbose=True,method=method)
        combine_cmd_list.append("./"+api.make_cmd(combineOption)+" >> combine_log.txt")
    combine_cmd = "\n".join(combine_cmd_list)
    worker = CrabWorker()
    crabConfig = CrabConfig(
            "CrabConfig",
            crab_file_path = os.path.join(crabDir,"combine_crab.py"),
            taskName = taskName,
            JobType_plugName = 'PrivateMC',
            JobType_psetName = 'os.environ[\'CMSSW_BASE\']+\'/src/CombineHarvester/CombineTools/scripts/do_nothing_cfg.py\'',
            JobType_scriptExe = 'combine_crab.sh',
            JobType_inputFiles = '[os.environ[\'CMSSW_BASE\']+\'/src/CombineHarvester/CombineTools/scripts/FrameworkJobReport.xml\', os.environ[\'CMSSW_BASE\']+\'/src/CombineHarvester/CombineTools/scripts/copyRemoteWorkspace.sh\', os.environ[\'CMSSW_BASE\']+\'/bin/\'+os.environ[\'SCRAM_ARCH\']+\'/combine\',]',
            JobType_outputFiles = '[\'combine_output.tar\',\'combine_log.txt\',]',
            Data_outputPrimaryDataset = 'Combine',
            Data_unitsPerJob = 1,
            Data_totalUnits = 1,
            Data_publication = False,
            Data_outputDatasetTag = '',
            #Data_outLFNDirBase = '\'/store/user/%s/HiggsCombine/\' % (getUsernameFromSiteDB()) + taskName + \'/{modelName}/\''.format(modelName=modelName,),
            Data_outLFNDirBase = '\'/store/user/{userName}/HiggsCombine/\' + taskName + \'/{modelName}/\''.format(userName=crabUserName,modelName=modelName,),
            Site_storageSite = 'T2_US_Florida',
            )
    execConfig = CrabConfig(
            "ExecConfig",
            exec_file_path = os.path.join(crabDir,"combine_crab.sh"),
            cmd_str = shell_script_template%(combine_cmd),
            )
    worker.make_exec_file(execConfig)
    worker.make_crab_file(crabConfig)
    if not dry_run:
        os.chdir(crabDir)
        worker.submit("combine_crab.py")
        os.chdir(pwdPath)
