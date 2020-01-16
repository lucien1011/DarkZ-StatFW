import glob,os,argparse,subprocess
from CombineAPI.CombineInterface import CombineAPI,CombineOption 
from Parametric.InputParameters import parameterDict
from BatchWorker.CondorWorker import CondorWorker,CondorConfig

parser = argparse.ArgumentParser()
parser.add_argument("--inputDir",action="store")
parser.add_argument("--selectStr",action="store")
parser.add_argument("--option",action="store",default="",type=str)
parser.add_argument("--pattern",action="store")
parser.add_argument("--method",action="store",default="AsymptoticLimits")
parser.add_argument("--batch",action="store_true")
parser.add_argument("--dry_run",action="store_true")
parser.add_argument("--njob",action="store",default=1,type=int)

option = parser.parse_args()

inputDir = option.inputDir
pattern = "window*.root" if not option.pattern else option.pattern

shell_script_template = """
#!/bin/bash
ulimit -s unlimited
set -e
echo "Setting up CMSSW"
cd {cmssw_base}/src
export SCRAM_ARCH={scram_arch}
source /cvmfs/cms.cern.ch/cmsset_default.sh
eval `scramv1 runtime -sh`
cd {pwd}
echo "Running combine"
{combine_cmd}
"""

api = CombineAPI()
for cardDir in glob.glob(inputDir+"*"+option.selectStr+"*/"):
    print "Running on directory "+cardDir
    if not option.batch:
        wsFilePath = cardDir+cardDir.split("/")[-2]+".root"
        optionList = option.option.split()
        combineOption = CombineOption(cardDir,wsFilePath,option=optionList,verbose=True,method=option.method)
        api.run(combineOption)
    else:
        wsFilePath = cardDir+cardDir.split("/")[-2]+".root"
        optionList = option.option.split()
        combineOption = CombineOption(cardDir,os.path.basename(wsFilePath),option=optionList,verbose=True,method=option.method)
        combine_cmd = api.make_cmd(combineOption)
        worker = CondorWorker()
        condorConfig = CondorConfig(
                "CondorConfig",
                condor_file_path = os.path.abspath(os.path.join(cardDir,"combine_condor.job")),
                exec_file_path = os.path.abspath(os.path.join(cardDir,"combine_condor.sh")),
                cmd_str = shell_script_template.format(
                    combine_cmd=combine_cmd,
                    cmssw_base=os.environ['CMSSW_BASE'],
                    scram_arch=os.environ['SCRAM_ARCH'],
                    pwd=os.environ['PWD'],
                    ),
                arguments = "",
                output = os.path.abspath(os.path.join(cardDir,"combine_condor.out")),
                error = os.path.abspath(os.path.join(cardDir,"combine_condor.err")),
                log = os.path.abspath(os.path.join(cardDir,"combine_condor.log")),
                njob = str(option.njob),
                input=os.path.abspath(wsFilePath),
                )
        worker.make_exec_file(condorConfig)
        worker.make_condor_file(condorConfig)
        if not option.dry_run: worker.submit(os.path.abspath(os.path.join(cardDir,"combine_condor.job")))

