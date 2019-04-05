#!/bin/bash

#python runCombineTask.py --inputDir DataCard/2018-10-23_Unblinding/ --selectStr "window"
#python runCombineTask.py --inputDir DataCard/2018-10-24_Unblinding/ --selectStr "window"
#python runCombineTask.py --inputDir DataCard/2018-10-25_Unblinding/ --selectStr "window"
#python runCombineTask.py --inputDir DataCard/2018-10-25_35p9_Unblinding/ --selectStr "window"
#python runCombineTask.py --inputDir DataCard/2018-10-24_Unblinding_NoSyst/ --selectStr "window" --option='--systematics=0'
#python runCombineTask.py --inputDir DataCard/2018-11-09_150p0_Unblinding/ --selectStr "window" --option "-t -1 --run=blind"
#python runCombineTask.py --inputDir DataCard/2018-11-09_150p0_Unblinding_NoSB/ --selectStr "window" --option "-t -1 --run=blind"
#python runCombineTask.py --inputDir DataCard/2018-11-15_150p0_Unblinding/ --selectStr "HZZd" --pattern "HZZd_M*.root"
#python runCombineTask.py --inputDir DataCard/2018-11-22_150p0_ParametricShape/ --selectStr "HZZd" --pattern "HZZd_M*.root"
#python runCombineTask.py --inputDir DataCard/2018-11-22_150p0_ParametricShape_v2/ --selectStr "HZZd" --pattern "HZZd_M*.root"
#python runCombineTask.py --inputDir DataCard/2018-11-26_150p0_ParametricShape_v2/ --selectStr "HZZd" --pattern "HZZd_M*.root" --option="-t -1 --run expected"

#python runCombineTask.py --inputDir DataCard/2018-11-26_150p0_ParametricShape_rebin_v2/ --selectStr "HZZd" --pattern "HZZd_M*.root" --method AsymptoticLimits --option "-t -1 --run expected --freezeParameters c0_Higgs,c1_Higgs,c2_Higgs,c3_Higgs,c4_Higgs,mean,width,c0_qqZZ,c1_qqZZ,c2_qqZZ,c3_qqZZ,c4_qqZZ,c0_ggZZ,c1_ggZZ,c2_ggZZ,c3_ggZZ,c4_ggZZ,meanVar_ZPlusX,widthVar_ZPlusX"
#python runCombineTask.py --inputDir DataCard/2018-11-26_150p0_ParametricShape_rebin_v4/ --selectStr "HZZd" --pattern "HZZd_M*.root" --method AsymptoticLimits --option "-t -1 --freezeParameters c0_Higgs,c1_Higgs,c2_Higgs,c3_Higgs,c4_Higgs,mean,width,c0_qqZZ,c1_qqZZ,c2_qqZZ,c3_qqZZ,c4_qqZZ,c0_ggZZ,c1_ggZZ,c2_ggZZ,c3_ggZZ,c4_ggZZ,meanVar_ZPlusX,widthVar_ZPlusX"

#python runCombineTask.py --inputDir DataCard/2018-11-26_150p0_ParametricShape_rebin_v5/ --selectStr "HZZd" --pattern "HZZd_M*.root" --method AsymptoticLimits --option "-t -1 --freezeParameters c0_Higgs,c1_Higgs,c2_Higgs,c3_Higgs,c4_Higgs,mean,width,c0_qqZZ,c1_qqZZ,c2_qqZZ,c3_qqZZ,c4_qqZZ,c0_ggZZ,c1_ggZZ,c2_ggZZ,c3_ggZZ,c4_ggZZ,meanVar_ZPlusX,widthVar_ZPlusX --run=blind"
#python runCombineTask.py --inputDir DataCard/2018-11-27_150p0_Unblinding_NoSB/ --selectStr "HZZd" --option "-t -1 --run=blind"
#python runCombineTask.py --inputDir DataCard/2018-11-27_150p0_Unblinding_NoSB_ParametricNumber/ --selectStr "HZZd" --option "-t -1 --run=blind"
#python runCombineTask.py --inputDir DataCard/2018-11-28_150p0_ParametricShape_rebin_v7/ --selectStr "HZZd" --option "-t -1 --run=blind"
#python runCombineTask.py --inputDir DataCard/2018-11-28_150p0_ParametricShape_rebin_v10/ --selectStr "HZZd" --option "-t -1 --run=blind --freezeParameters c0_Higgs,c1_Higgs,c2_Higgs,c3_Higgs,c4_Higgs,mean,width,alphaL,alphaR,nL,nR,c0_qqZZ,c1_qqZZ,c2_qqZZ,c3_qqZZ,c4_qqZZ,c0_ggZZ,c1_ggZZ,c2_ggZZ,c3_ggZZ,c4_ggZZ,meanVar_ZPlusX,widthVar_ZPlusX"
#python runCombineTask.py --inputDir DataCard/2018-11-28_150p0_ParametricShape_rebin_v10/ --selectStr "HZZd" --option "-t -1 --run=blind --freezeParameters c0_Higgs_Mu,c1_Higgs_Mu,c2_Higgs_Mu,c3_Higgs_Mu,c4_Higgs_Mu,mean_Mu,width_Mu,alphaL_Mu,alphaR_Mu,nL_Mu,nR_Mu,c0_qqZZ_Mu,c1_qqZZ_Mu,c2_qqZZ_Mu,c3_qqZZ_Mu,c4_qqZZ_Mu,c0_ggZZ_Mu,c1_ggZZ_Mu,c2_ggZZ_Mu,c3_ggZZ_Mu,c4_ggZZ_Mu,meanVar_ZPlusX_Mu,widthVar_ZPlusX,c0_Higgs_El,c1_Higgs_El,c2_Higgs_El,c3_Higgs_El,c4_Higgs_El,mean_El,width_El,alphaL_El,alphaR_El,nL_El,nR_El,c0_qqZZ_El,c1_qqZZ_El,c2_qqZZ_El,c3_qqZZ_El,c4_qqZZ_El,c0_ggZZ_El,c1_ggZZ_El,c2_ggZZ_El,c3_ggZZ_El,c4_ggZZ_El,meanVar_ZPlusX_El,widthVar_ZPlusX"

#python runCombineTask.py --inputDir DataCard/2018-11-29_150p0_ParametricShape_SignalDCB/ --selectStr "HZZd" --option "-t -1 --run=blind --freezeParameters c0_Higgs_Mu,c1_Higgs_Mu,c2_Higgs_Mu,c3_Higgs_Mu,c4_Higgs_Mu,mean_Mu,width_Mu,alphaL_Mu,alphaR_Mu,nL_Mu,nR_Mu,c0_qqZZ_Mu,c1_qqZZ_Mu,c2_qqZZ_Mu,c3_qqZZ_Mu,c4_qqZZ_Mu,c0_ggZZ_Mu,c1_ggZZ_Mu,c2_ggZZ_Mu,c3_ggZZ_Mu,c4_ggZZ_Mu,meanVar_ZPlusX_Mu,widthVar_ZPlusX,c0_Higgs_El,c1_Higgs_El,c2_Higgs_El,c3_Higgs_El,c4_Higgs_El,mean_El,width_El,alphaL_El,alphaR_El,nL_El,nR_El,c0_qqZZ_El,c1_qqZZ_El,c2_qqZZ_El,c3_qqZZ_El,c4_qqZZ_El,c0_ggZZ_El,c1_ggZZ_El,c2_ggZZ_El,c3_ggZZ_El,c4_ggZZ_El,meanVar_ZPlusX_El,widthVar_ZPlusX"
#python runCombineTask.py --inputDir DataCard/2018-11-28_150p0_Unblinding_NoSB/ --selectStr "HZZd" --option "-t -1 --run=blind"

#python runCombineTask.py --inputDir DataCard/2018-11-30_150p0_ParametricShape_SignalDCB_HiggsRateParam/ --selectStr "HZZd" --option "-t -1 --run=blind --freezeParameters c0_Higgs_Mu,c1_Higgs_Mu,c2_Higgs_Mu,c3_Higgs_Mu,c4_Higgs_Mu,mean_Mu,width_Mu,alphaL_Mu,alphaR_Mu,nL_Mu,nR_Mu,c0_qqZZ_Mu,c1_qqZZ_Mu,c2_qqZZ_Mu,c3_qqZZ_Mu,c4_qqZZ_Mu,c0_ggZZ_Mu,c1_ggZZ_Mu,c2_ggZZ_Mu,c3_ggZZ_Mu,c4_ggZZ_Mu,meanVar_ZPlusX_Mu,widthVar_ZPlusX_Mu,c0_Higgs_El,c1_Higgs_El,c2_Higgs_El,c3_Higgs_El,c4_Higgs_El,mean_El,width_El,alphaL_El,alphaR_El,nL_El,nR_El,c0_qqZZ_El,c1_qqZZ_El,c2_qqZZ_El,c3_qqZZ_El,c4_qqZZ_El,c0_ggZZ_El,c1_ggZZ_El,c2_ggZZ_El,c3_ggZZ_El,c4_ggZZ_El,meanVar_ZPlusX_El,widthVar_ZPlusX_El"
#python runCombineTask.py --inputDir DataCard/2018-11-30_150p0_Unblinding/ --selectStr "HZZd" --option "-t -1 --run=blind"
#python runCombineTask.py --inputDir DataCard/2018-11-30_150p0_Unblinding_NoSB/ --selectStr "HZZd" --option "-t -1 --run=blind"
#python runCombineTask.py --inputDir DataCard/2018-11-30_150p0_ParametricShape_SignalDCB/ --selectStr "HZZd" --option "-t -1 --run=blind --freezeParameters c0_Higgs_Mu,c1_Higgs_Mu,c2_Higgs_Mu,c3_Higgs_Mu,c4_Higgs_Mu,mean_Mu,width_Mu,alphaL_Mu,alphaR_Mu,nL_Mu,nR_Mu,c0_qqZZ_Mu,c1_qqZZ_Mu,c2_qqZZ_Mu,c3_qqZZ_Mu,c4_qqZZ_Mu,c0_ggZZ_Mu,c1_ggZZ_Mu,c2_ggZZ_Mu,c3_ggZZ_Mu,c4_ggZZ_Mu,meanVar_ZPlusX_Mu,widthVar_ZPlusX_Mu,c0_Higgs_El,c1_Higgs_El,c2_Higgs_El,c3_Higgs_El,c4_Higgs_El,mean_El,width_El,alphaL_El,alphaR_El,nL_El,nR_El,c0_qqZZ_El,c1_qqZZ_El,c2_qqZZ_El,c3_qqZZ_El,c4_qqZZ_El,c0_ggZZ_El,c1_ggZZ_El,c2_ggZZ_El,c3_ggZZ_El,c4_ggZZ_El,meanVar_ZPlusX_El,widthVar_ZPlusX_El"
#python runCombineTask.py --inputDir DataCard/2018-11-30_150p0_ParametricShape_SignalDCB_HiggsRateParam/ --selectStr "HZZd_M4" --option "-t -1 --run=blind --freezeParameters c0_Higgs_Mu,c1_Higgs_Mu,c2_Higgs_Mu,c3_Higgs_Mu,c4_Higgs_Mu,mean_Mu,width_Mu,alphaL_Mu,alphaR_Mu,nL_Mu,nR_Mu,c0_qqZZ_Mu,c1_qqZZ_Mu,c2_qqZZ_Mu,c3_qqZZ_Mu,c4_qqZZ_Mu,c0_ggZZ_Mu,c1_ggZZ_Mu,c2_ggZZ_Mu,c3_ggZZ_Mu,c4_ggZZ_Mu,meanVar_ZPlusX_Mu,widthVar_ZPlusX_Mu,c0_Higgs_El,c1_Higgs_El,c2_Higgs_El,c3_Higgs_El,c4_Higgs_El,mean_El,width_El,alphaL_El,alphaR_El,nL_El,nR_El,c0_qqZZ_El,c1_qqZZ_El,c2_qqZZ_El,c3_qqZZ_El,c4_qqZZ_El,c0_ggZZ_El,c1_ggZZ_El,c2_ggZZ_El,c3_ggZZ_El,c4_ggZZ_El,meanVar_ZPlusX_El,widthVar_ZPlusX_El"
#python runCombineTask.py --inputDir DataCard/2019-03-29_136p1_ParametricShape_SignalDCB_HiggsRateParam/ --selectStr "HZZd_M" --option "-t -1 --run=blind --freezeParameters c0_Higgs_Mu,c1_Higgs_Mu,c2_Higgs_Mu,c3_Higgs_Mu,c4_Higgs_Mu,mean_Mu,width_Mu,alphaL_Mu,alphaR_Mu,nL_Mu,nR_Mu,c0_qqZZ_Mu,c1_qqZZ_Mu,c2_qqZZ_Mu,c3_qqZZ_Mu,c4_qqZZ_Mu,c0_ggZZ_Mu,c1_ggZZ_Mu,c2_ggZZ_Mu,c3_ggZZ_Mu,c4_ggZZ_Mu,meanVar_ZPlusX_Mu,widthVar_ZPlusX_Mu,c0_Higgs_El,c1_Higgs_El,c2_Higgs_El,c3_Higgs_El,c4_Higgs_El,mean_El,width_El,alphaL_El,alphaR_El,nL_El,nR_El,c0_qqZZ_El,c1_qqZZ_El,c2_qqZZ_El,c3_qqZZ_El,c4_qqZZ_El,c0_ggZZ_El,c1_ggZZ_El,c2_ggZZ_El,c3_ggZZ_El,c4_ggZZ_El,meanVar_ZPlusX_El,widthVar_ZPlusX_El"
#python runCombineTask.py --inputDir DataCard/2019-04-04_136p1_CutAndCount_HiggsRateParam/ --selectStr "Zd_MZD" --option "-t -1 --run=blind"
#python runCombineTask.py --inputDir DataCard/2019-04-04_136p1_CutAndCount_ppToZZd_HiggsRateParam/ --selectStr "Zd_MZD" --option "-t -1 --run=blind --redefineSignalPOIs epsilon --freezeParameters r"
#python runCombineTask.py --inputDir DataCard/2019-04-04_136p1_CutAndCount_EpsilonInDC_HiggsRateParam/ --selectStr "Zd_MZD" --option "-t -1 --run=blind --redefineSignalPOIs epsilon --freezeParameters r"
python runCombineTask.py --inputDir DataCard/2019-04-04_136p1_CutAndCount_qqZZXs0p04pb_HiggsRateParam/ --selectStr "Zd_MZD" --option "-t -1 --run=blind --redefineSignalPOIs epsilon --freezeParameters r"

# ===============================================================
# Cards for HToZdZd
# ===============================================================
#python runCombineTask.py --inputDir HToZdZd_DataCard/2019-02-13_test_RatioCut0p05/ --selectStr "HToZdZd_MZD" --option "-t -1 --run=blind"
#python runCombineTask.py --inputDir HToZdZd_DataCard/2019-02-14_35p9_RatioCut0p05/ --selectStr "HToZdZd_MZD" --option "-t -1 --run=blind"
#python runCombineTask.py --inputDir HToZdZd_DataCard/2019-02-15_35p9_RatioCut0p05_MCStatUnc_Width0p05/ --selectStr "HToZdZd_MZD" --option "-t -1 --run=blind"
#python runCombineTask.py --inputDir HToZdZd_DataCard/2019-02-18_35p9_RatioCut0p05_MCStatUnc_Width0p01And0p02/ --selectStr "HToZdZd_MZD" --option "-t -1 --run=blind"
#python runCombineTask.py --inputDir HToZdZd_DataCard/2019-02-18_35p9_RatioCut0p02And0p01_MCStatUnc/ --selectStr "HToZdZd_MZD" --option "-t -1 --run=blind"
#python runCombineTask.py --inputDir HToZdZd_DataCard/2019-02-28_35p9_RatioCut0p05_MCStatUnc_Width0p02And0p05/ --selectStr "HToZdZd_MZD" --option "-t -1 --run=blind"
#python runCombineTask.py --inputDir HToZdZd_DataCard/2019-03-29_136p1_RatioCut0p05/ --selectStr "HToZdZd_MZD" --option "-t -1 --run=blind"
