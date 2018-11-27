#!/bin/bash

#python runCombineTask.py --inputDir DataCard/2018-10-23_Unblinding/ --selectStr "window"
#python runCombineTask.py --inputDir DataCard/2018-10-24_Unblinding/ --selectStr "window"
#python runCombineTask.py --inputDir DataCard/2018-10-25_Unblinding/ --selectStr "window"
#python runCombineTask.py --inputDir DataCard/2018-10-25_35p9_Unblinding/ --selectStr "window"
#python runCombineTask.py --inputDir DataCard/2018-10-24_Unblinding_NoSyst/ --selectStr "window" --option='--systematics=0'
#python runCombineTask.py --inputDir DataCard/2018-11-09_150p0_Unblinding/ --selectStr "window"
#python runCombineTask.py --inputDir DataCard/2018-11-15_150p0_Unblinding_NoSB/ --selectStr "HZZd" --pattern "HZZd_M*.root"
#python runCombineTask.py --inputDir DataCard/2018-11-15_150p0_Unblinding/ --selectStr "HZZd" --pattern "HZZd_M*.root"
#python runCombineTask.py --inputDir DataCard/2018-11-22_150p0_ParametricShape/ --selectStr "HZZd" --pattern "HZZd_M*.root"
#python runCombineTask.py --inputDir DataCard/2018-11-22_150p0_ParametricShape_v2/ --selectStr "HZZd" --pattern "HZZd_M*.root"
#python runCombineTask.py --inputDir DataCard/2018-11-26_150p0_ParametricShape_v2/ --selectStr "HZZd" --pattern "HZZd_M*.root" --option="-t -1 --run expected"

#python runCombineTask.py --inputDir DataCard/2018-11-26_150p0_ParametricShape_rebin_v2/ --selectStr "HZZd" --pattern "HZZd_M*.root" --method AsymptoticLimits --option "-t -1 --run expected --freezeParameters c0_Higgs,c1_Higgs,c2_Higgs,c3_Higgs,c4_Higgs,mean,width,c0_qqZZ,c1_qqZZ,c2_qqZZ,c3_qqZZ,c4_qqZZ,c0_ggZZ,c1_ggZZ,c2_ggZZ,c3_ggZZ,c4_ggZZ,meanVar_ZPlusX,widthVar_ZPlusX"
#python runCombineTask.py --inputDir DataCard/2018-11-26_150p0_ParametricShape_rebin_v4/ --selectStr "HZZd" --pattern "HZZd_M*.root" --method AsymptoticLimits --option "-t -1 --freezeParameters c0_Higgs,c1_Higgs,c2_Higgs,c3_Higgs,c4_Higgs,mean,width,c0_qqZZ,c1_qqZZ,c2_qqZZ,c3_qqZZ,c4_qqZZ,c0_ggZZ,c1_ggZZ,c2_ggZZ,c3_ggZZ,c4_ggZZ,meanVar_ZPlusX,widthVar_ZPlusX"

python runCombineTask.py --inputDir DataCard/2018-11-26_150p0_ParametricShape_rebin_v5/ --selectStr "HZZd" --pattern "HZZd_M*.root" --method AsymptoticLimits --option "-t -1 --freezeParameters c0_Higgs,c1_Higgs,c2_Higgs,c3_Higgs,c4_Higgs,mean,width,c0_qqZZ,c1_qqZZ,c2_qqZZ,c3_qqZZ,c4_qqZZ,c0_ggZZ,c1_ggZZ,c2_ggZZ,c3_ggZZ,c4_ggZZ,meanVar_ZPlusX,widthVar_ZPlusX"
