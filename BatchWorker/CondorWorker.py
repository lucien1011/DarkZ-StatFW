from .Worker import Worker
from .Site import Site
from .BaseObject import BaseObject
from mkdir_p import mkdir_p
import os

condor_file_template = """universe = vanilla
executable          = {exec_file_path}
arguments           = "{arguments}"
input               = {input}
output              = {output}
error               = {error}
log                 = {log}
# Send the job to Held state on failure.
on_exit_hold = (ExitBySignal == True) || (ExitCode != 0)
# Periodically retry the jobs every 10 minutes, up to a maximum of 5 retries.
periodic_release =  (NumJobStarts < 3) && ((CurrentTime - EnteredCurrentStatus) > 600)
queue {njob}
"""

class CondorConfig(BaseObject):
    def __init__(self,name,**kwargs):
        super(CondorConfig,self).__init__(name,**kwargs)

class CondorWorker(Worker):
    def __init__(self):
        super(CondorWorker,self).__init__()

    def make_exec_file(self,condorConfig):
        outputPath = condorConfig.exec_file_path
        cmd_str = condorConfig.cmd_str
        mkdir_p(os.path.dirname(outputPath))
        outputFile = open(outputPath,"w")
        outputFile.write(cmd_str)
        outputFile.close()

    def make_condor_file(self,condorConfig):
        outputPath = condorConfig.condor_file_path
        mkdir_p(os.path.dirname(outputPath))
        condor_file_content = condor_file_template.format(
                exec_file_path = condorConfig.exec_file_path,
                arguments = condorConfig.arguments,
                input = condorConfig.input,
                output = condorConfig.output,
                error = condorConfig.error,
                log = condorConfig.log,
                njob = condorConfig.njob,
                )
        outputFile = open(outputPath,"w")
        outputFile.write(condor_file_content)
        outputFile.close()

    def submit(self,condor_config_path):
        os.system("condor_submit "+condor_config_path)
