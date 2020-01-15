import glob,os,argparse
from BatchWorker.CondorWorker import CondorWorker,CondorConfig

parser = argparse.ArgumentParser()
parser.add_argument("--inputDir",action="store")
parser.add_argument("--cardName",action="store",default="window.txt")
parser.add_argument("--combinePattern",action="store",default="")
parser.add_argument("--batch",action="store_true")

option = parser.parse_args()

inputDir = option.inputDir

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
            condor_file_path = os.path.abspath(os.path.join(inputDir,"mk_ws_condor.job")),
            exec_file_path = os.path.abspath(os.path.join(inputDir,"mk_ws_condor.sh")),
            cmd_str = """
#!/bin/bash
{combine_card_cmd}
{mk_ws_cmd}
""".format(combine_card_cmd=combine_card_cmd,mk_ws_cmd=mk_ws_cmd,),
            arguments = "",
            output = os.path.abspath(os.path.join(inputDir,"mk_ws_condor.out")),
            error = os.path.abspath(os.path.join(inputDir,"mk_ws_condor.err")),
            log = os.path.abspath(os.path.join(inputDir,"mk_ws_condor.log")),
            )
    worker.make_exec_file(condorConfig)
    worker.make_condor_file(condorConfig)
    worker.submit(os.path.abspath(os.path.join(inputDir,"mk_ws_condor.job")))
else:
    os.system(cmd)

