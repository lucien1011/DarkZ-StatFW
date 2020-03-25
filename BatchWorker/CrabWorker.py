from .Worker import Worker
from .Site import Site
from .BaseObject import BaseObject
from mkdir_p import mkdir_p
import os

crab_file_template = """import os
from WMCore.Configuration import Configuration
from CRABClient.UserUtilities import config, getUsernameFromSiteDB

config = Configuration()
taskName                            = '{taskName}'

config.section_('General')
config.General.requestName          = taskName

config.section_('JobType')
config.JobType.pluginName           = '{JobType_plugName}'
config.JobType.psetName             = {JobType_psetName}
config.JobType.scriptExe            = '{JobType_scriptExe}'
config.JobType.inputFiles           = {JobType_inputFiles}
config.JobType.outputFiles          = {JobType_outputFiles}
config.JobType.maxMemoryMB          = {JobType_maxMemoryMB}

config.section_('Data')
config.Data.outputPrimaryDataset    = '{Data_outputPrimaryDataset}'
config.Data.splitting               = 'EventBased'
config.Data.unitsPerJob             = {Data_unitsPerJob}
config.Data.totalUnits              = {Data_totalUnits}
config.Data.publication             = {Data_publication}
config.Data.outputDatasetTag        = '{Data_outputDatasetTag}'
config.Data.outLFNDirBase           = {Data_outLFNDirBase}

config.section_('User')

config.section_('Site')
config.Site.storageSite = '{Site_storageSite}'
"""

class CrabConfig(BaseObject):
    def __init__(self,name,**kwargs):
        super(CrabConfig,self).__init__(name,**kwargs)

class CrabWorker(Worker):
    def __init__(self):
        super(CrabWorker,self).__init__()

    def make_crab_file(self,crabConfig):
        outputPath = crabConfig.crab_file_path
        mkdir_p(os.path.dirname(outputPath))
        crab_file_content = crab_file_template.format(
                taskName = crabConfig.taskName,
                JobType_plugName = crabConfig.JobType_plugName,
                JobType_psetName = crabConfig.JobType_psetName,
                JobType_scriptExe = crabConfig.JobType_scriptExe,
                JobType_inputFiles = crabConfig.JobType_inputFiles,
                JobType_outputFiles = crabConfig.JobType_outputFiles,
                JobType_maxMemoryMB = crabConfig.JobType_maxMemoryMB,
                Data_outputPrimaryDataset = crabConfig.Data_outputPrimaryDataset,
                Data_unitsPerJob = crabConfig.Data_unitsPerJob,
                Data_totalUnits = crabConfig.Data_totalUnits,
                Data_publication = crabConfig.Data_publication,
                Data_outputDatasetTag = crabConfig.Data_outputDatasetTag,
                Data_outLFNDirBase = crabConfig.Data_outLFNDirBase,
                Site_storageSite = crabConfig.Site_storageSite,
                )
        outputFile = open(outputPath,"w")
        outputFile.write(crab_file_content)
        outputFile.close()

    def make_exec_file(self,config):
        outputPath = config.exec_file_path
        cmd_str = config.cmd_str
        mkdir_p(os.path.dirname(outputPath))
        outputFile = open(outputPath,"w")
        outputFile.write(cmd_str)
        outputFile.close()

    def submit(self,crab_config_path):
        os.system("crab submit -c "+crab_config_path)
        
