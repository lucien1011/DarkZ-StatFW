import glob,os,argparse,subprocess,ROOT
from collections import OrderedDict
from CombineAPI.CombineInterface import CombineAPI,CombineOption 
from Parametric.InputParameters import parameterDict
from BatchWorker.CrabWorker import CrabWorker,CrabConfig
from Utilities.mkdir_p import mkdir_p
from StatFW.BaseObject import BaseObject

# ____________________________________________________________________________________________________________________________________________ ||
#inputDir        = "/cms/data/store/user/klo/HiggsCombineWorkspace/HIG-19-007/XX_2020-03-03_SR2D_RunII/"
#taskName        = "2020-03-06_SR2D_RunII"

#inputDir        = "/cms/data/store/user/klo/HiggsCombineWorkspace/HIG-19-007/XX_2020-03-17_SR2D_RunII/"
#taskName        = "2020-03-17_SR2D_RunII_LHCLimit_v2"
#taskName        = "2020-03-17_SR2D_RunII_LHCLimit_v2_ext1"
#asymLimitDir    = "/home/lucien/AnalysisCode/Higgs/DarkZ-StatFW/HToZdZd_DataCard/2020-03-17_SR2D_RunII/"

#inputDir        = "/cms/data/store/user/klo/HiggsCombineWorkspace/HIG-19-007/XX_2020-03-17_SR2D_RunII_El/"
#taskName        = "2020-03-17_SR2D_RunII_El_LHCLimit_v2"
#asymLimitDir    = "/home/lucien/AnalysisCode/Higgs/DarkZ-StatFW/HToZdZd_DataCard/2020-03-17_SR2D_RunII_El/"

#inputDir        = "/cms/data/store/user/klo/HiggsCombineWorkspace/HIG-19-007/XX_2020-03-17_SR2D_RunII_Mu/"
#taskName        = "2020-03-17_SR2D_RunII_Mu_LHCLimit_v2"
#asymLimitDir    = "/home/lucien/AnalysisCode/Higgs/DarkZ-StatFW/HToZdZd_DataCard/2020-03-17_SR2D_RunII_Mu/"

#inputDir        = "/cms/data/store/user/klo/HiggsCombineWorkspace/HIG-19-007/ZX_2020-03-03_CutAndCount_m4lSR-HZZd_RunII/"
#taskName        = "2020-03-03_CutAndCount_m4lSR-HZZd_RunII_LHCLimit_v2"
#asymLimitDir    = "/home/lucien/AnalysisCode/Higgs/DarkZ-StatFW/DataCard/2020-03-03_CutAndCount_m4lSR-HZZd_RunII/"

#inputDir        = "/cms/data/store/user/klo/HiggsCombineWorkspace/HIG-19-007/ZX_2020-03-03_CutAndCount_m4lSR-HZZd_RunII_Mu/"
#taskName        = "2020-03-03_CutAndCount_m4lSR-HZZd_RunII_Mu_LHCLimit_v2"
#asymLimitDir    = "/home/lucien/AnalysisCode/Higgs/DarkZ-StatFW/DataCard/2020-03-03_CutAndCount_m4lSR-HZZd_RunII_Mu/"

inputDir        = "/cms/data/store/user/klo/HiggsCombineWorkspace/HIG-19-007/ZX_2020-03-03_CutAndCount_m4lSR-HZZd_RunII_El/"
taskName        = "2020-03-03_CutAndCount_m4lSR-HZZd_RunII_El_LHCLimit_v2"
asymLimitDir    = "/home/lucien/AnalysisCode/Higgs/DarkZ-StatFW/DataCard/2020-03-03_CutAndCount_m4lSR-HZZd_RunII_El/"

# ____________________________________________________________________________________________________________________________________________ ||
#mass_points     = [4,5,6,7,8,9,10,15,20,25,30,35,40,45,50,55,60]
#mass_points     = [4.20*1.005**i for i in range(541)]
mass_points     = [4.04*1.005**i for i in range(434)]
crabTaskDir     = "crabTaskDir/"
dry_run         = False
method          = "HybridNew"
scan_option     = "--LHCmode=LHC-limits --clsAcc 0 -T 3000 --saveHybridResult -s -1 --rMax 200"
compute_option  = "--LHCmode LHC-limits -T 3000 --readHybridResults --grid gridd.root"
crabUserName    = "klo"
maxMemoryMB     = 4000
exec_dir        = "./"
#exec_dir        = "$CMSSW_BASE/src/CombineHarvester/CombineTools/scripts/"
useHarvester    = False
#points_to_scan  = [0.1+0.25*i for i in range(21)]
points_to_scan  = [0.1+0.25*i for i in range(21)]+[5.5+0.5*i for i in range(10)]
useAsymAsStart  = True
n_asym_scan     = 20

# ____________________________________________________________________________________________________________________________________________ ||
quantiles       = [
    BaseObject("down2",
        asymp_file_name="higgsCombineTest.AsymptoticLimits.mH120.root",
        hybridnew_file_name="higgsCombineTest.HybridNew.mH120.quant0.025.root",
        ),
    BaseObject("down1",
        asymp_file_name="higgsCombineTest.AsymptoticLimits.mH120.root",
        hybridnew_file_name="higgsCombineTest.HybridNew.mH120.quant0.160.root",
        ),
    BaseObject("central",
        asymp_file_name="higgsCombineTest.AsymptoticLimits.mH120.root",
        hybridnew_file_name="higgsCombineTest.HybridNew.mH120.quant0.500.root",
        ),
    BaseObject("up1",
        asymp_file_name="higgsCombineTest.AsymptoticLimits.mH120.root",
        hybridnew_file_name="higgsCombineTest.HybridNew.mH120.quant0.840.root",
        ),
    BaseObject("up2",
        asymp_file_name="higgsCombineTest.AsymptoticLimits.mH120.root",
        hybridnew_file_name="higgsCombineTest.HybridNew.mH120.quant0.975.root",
        ),
    BaseObject("obs",
        asymp_file_name="higgsCombineTest.AsymptoticLimits.mH120.root",
        hybridnew_file_name="higgsCombineTest.HybridNew.mH120.root",
        ),
    ]
if useAsymAsStart and asymLimitDir:
    asymLimitDict = OrderedDict()
    for quantile in quantiles:
        asymLimitDict[quantile.name] = OrderedDict()
    for cardDir in glob.glob(asymLimitDir+"*/"):
        print "Reading directory "+cardDir
        window_name = cardDir.split("/")[-2]
        window_value = float(window_name.split("_")[1].replace("MZD",""))
        for i,quan in enumerate(quantiles):
            inputFile = ROOT.TFile(cardDir+quan.asymp_file_name,"READ")
            tree = inputFile.Get("limit")
            tree.GetEntry(i)
            asymLimitDict[quan.name][window_name] = getattr(tree,"limit")
            inputFile.Close()
else:
    asymLimitDict = {}

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
tar -cf combine_pdf.tar *.pdf
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
    combine_cmd_list = []
    wsFilePathRoot = wsFilePath.replace("/cms/data","root://cms-xrd-global.cern.ch/")
    combine_cmd_list.append('./copyRemoteWorkspace.sh %s ./%s ' % (wsFilePathRoot, os.path.basename(wsFilePathRoot)))
    if asymLimitDict:
        median = asymLimitDict["central"][modelName]
        up2 = asymLimitDict["up2"][modelName]
        down2 = asymLimitDict["down2"][modelName]
        interval = abs(up2-down2)/n_asym_scan
        print "Asymptotic median limit: ",median
        print "Asymptotic up2 limit: ",up2
        print "Asymptotic down2 limit: ",down2
        print "Interval used: ",interval
        points_to_scan_low = [median-i*interval for i in range(n_asym_scan+1) if median-i*interval>0.]
        if len(points_to_scan_low) < n_asym_scan:
            points_to_scan_low += [min(points_to_scan_low)-i*0.1 for i in range(1,11) if min(points_to_scan_low)-i*0.1>0.]
        points_to_scan = points_to_scan_low+[median+i*interval for i in range(1,n_asym_scan+1)]
    for point_to_scan in points_to_scan:
        combineOption = CombineOption(crabDir,os.path.basename(wsFilePath),option=scan_option.split()+["--singlePoint=%s"%point_to_scan,"-n","FullCLs.POINT.%s"%point_to_scan,],verbose=True,method=method,useHarvester=useHarvester)
        combine_cmd_list.append(exec_dir+api.make_cmd(combineOption)+" >> combine_log.txt")
    combine_cmd_list.append("hadd gridd.root higgsCombineFullCLs.POINT.*.root")
    combineOption = CombineOption(crabDir,os.path.basename(wsFilePath),option=compute_option.split(),verbose=True,method=method)
    combine_cmd_list.append(exec_dir+api.make_cmd(combineOption)+" >> combine_log.txt")
    for quantile in [0.500,0.840,0.160,0.975,0.025]:
        combineOption = CombineOption(crabDir,os.path.basename(wsFilePath),option=compute_option.split()+["--expectedFromGrid="+str(quantile),"--plot=cls_fromgrid_exp"+str(quantile)+".pdf"],verbose=True,method=method)
        combine_cmd_list.append(exec_dir+api.make_cmd(combineOption)+" >> combine_log.txt")
    combine_cmd = "\n".join(combine_cmd_list)
    worker = CrabWorker()
    crabConfig = CrabConfig(
            "CrabConfig",
            crab_file_path = os.path.join(crabDir,"combine_crab.py"),
            taskName = taskName,
            JobType_plugName = 'PrivateMC',
            JobType_psetName = 'os.environ[\'CMSSW_BASE\']+\'/src/CombineHarvester/CombineTools/scripts/do_nothing_cfg.py\'',
            JobType_scriptExe = 'combine_crab.sh',
            JobType_inputFiles = '[os.environ[\'CMSSW_BASE\']+\'/src/CombineHarvester/CombineTools/scripts/FrameworkJobReport.xml\', os.environ[\'CMSSW_BASE\']+\'/src/CombineHarvester/CombineTools/scripts/copyRemoteWorkspace.sh\', os.environ[\'CMSSW_BASE\']+\'/bin/\'+os.environ[\'SCRAM_ARCH\']+\'/combine\', os.environ[\'CMSSW_BASE\']+\'/src/CombineHarvester/CombineTools/scripts/combineTool.py\',]',
            JobType_outputFiles = '[\'combine_output.tar\',\'combine_log.txt\', \'combine_pdf.tar\']',
            JobType_maxMemoryMB = str(maxMemoryMB),
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
