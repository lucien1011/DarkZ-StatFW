from .Worker import Worker
from .Site import Site
from .BaseObject import BaseObject
from mkdir_p import mkdir_p
import os

condor_file_template = """
executable          = {exec_file_path}
arguments           = "{arguments}"
output              = {output}
error               = {error}
log                 = {log}
queue
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
                output = condorConfig.output,
                error = condorConfig.error,
                log = condorConfig.log,
                )
        outputFile = open(outputPath,"w")
        outputFile.write(condor_file_content)
        outputFile.close()

    def submit(self,condor_config_path):
        os.system("condor_submit "+condor_config_path)
