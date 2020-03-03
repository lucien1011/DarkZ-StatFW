import glob,os,argparse
from BatchWorker.CondorWorker import CondorWorker,CondorConfig

parser = argparse.ArgumentParser()
parser.add_argument("--inputDir",action="store")
parser.add_argument("--cardName",action="store",default="window.txt")
parser.add_argument("--combinePattern",action="store",default="")
parser.add_argument("--njob",action="store",default=1,type=int)
parser.add_argument("--batch",action="store_true")
parser.add_argument("--dry_run",action="store_true")

option = parser.parse_args()

inputDir = option.inputDir

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
echo "Combining data cards"
{combine_card_cmd}
echo "Making workspace"
{mk_ws_cmd}
"""

textFileName = os.path.abspath(os.path.join(inputDir,option.cardName))
print "*"*20
if option.combinePattern:
    print "Combining datacard with pattern in file name", option.combinePattern
    chStr = ""
    for each_ch_name in glob.glob(inputDir+option.combinePattern):
        chStr += " "+os.path.basename(each_ch_name).replace(".txt","")+"="+os.path.abspath(each_ch_name)
    combine_card_cmd = "combineCards.py "+chStr+" > "+textFileName
    print combine_card_cmd
    if not option.batch:
        os.system(combine_card_cmd)
print "Making workspace from", textFileName
mk_ws_cmd = "text2workspace.py "+textFileName+" -v 1 --no-b-only"
print mk_ws_cmd
if option.batch:
    worker = CondorWorker()
    condorConfig = CondorConfig(
            "CondorConfig",
            #condor_file_path = os.path.abspath(os.path.join(inputDir,"mk_ws_condor.job")),
            #exec_file_path = os.path.abspath(os.path.join(inputDir,"mk_ws_condor.sh")),
            condor_file_path = "mk_ws_condor.job",
            exec_file_path = "mk_ws_condor.sh",
            cmd_str = shell_script_template.format(
                combine_card_cmd=combine_card_cmd,
                mk_ws_cmd=mk_ws_cmd,
                cmssw_base=os.environ['CMSSW_BASE'],
                scram_arch=os.environ['SCRAM_ARCH'],
                pwd=os.environ['PWD'],
                ),
            arguments = "",
            #output = os.path.abspath(os.path.join(inputDir,"mk_ws_condor.out")),
            #error = os.path.abspath(os.path.join(inputDir,"mk_ws_condor.err")),
            #log = os.path.abspath(os.path.join(inputDir,"mk_ws_condor.log")),
            output = "mk_ws_condor.out",
            error = "mk_ws_condor.err",
            log = "mk_ws_condor.log",
            njob = str(option.njob),
            )
    worker.make_exec_file(condorConfig)
    worker.make_condor_file(condorConfig)
    if not option.dry_run: worker.submit(os.path.abspath(os.path.join(inputDir,"mk_ws_condor.job")))
else:
    os.system(mk_ws_cmd)

