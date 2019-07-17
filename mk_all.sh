#!/bin/bash

# ________________________________________________________________________________________________________________________ ||
#inputDir=/raid/raid7/lucien/Higgs/DarkZ/ParaInput/DarkPhotonSelection_m4l100To170_Nominal/2019-05-09_m4lSR-m4lLowSB-m4lHighSB_HZZd-ppZZd/
#inputDir=/raid/raid7/lucien/Higgs/DarkZ/ParaInput/DarkPhotonSelection_m4l100To170_Nominal/2019-05-09_m4lSR-m4lSB_HZZd-ppZZd/
#inputDir=/raid/raid7//lucien/Higgs/DarkZ/ParaInput/DarkPhotonSelection_m4l100To170_Nominal/2019-05-15_m4lSR-m4lSB_HZZd-ppZZd/
#inputDir=/raid/raid7//lucien/Higgs/DarkZ/ParaInput/DarkPhotonSelection_m4l100To170_Nominal/2019-07-08_m4lSR-m4lSB_HZZd-ppZZd/
#inputDir=/raid/raid7/lucien/Higgs/DarkZ/ParaInput/DarkPhotonSelection_m4l100To170_Nominal/2019-07-09_m4lSR-m4lSB_HZZd-ppZZd/
#inputDir=/raid/raid7//lucien/Higgs/DarkZ/ParaInput/DarkPhotonSelection_m4l100To170_Nominal/2019-07-09_m4lSR-m4lSB_ppZZd_scaleZX/
#inputDir=/raid/raid7//lucien/Higgs/DarkZ/ParaInput/DarkPhotonSelection_m4l100To170_Nominal/2019-07-09_m4lSR-m4lSB_ppZZd_Run2016/
inputDir=/raid/raid7/lucien/Higgs/DarkZ/ParaInput/DarkPhotonSelection_m4l100To170_Nominal/2019-07-17_m4lSR-m4lSB_HZZd-ppZZd_Run2016/
#inputDir=/raid/raid7/lucien/Higgs/DarkZ/ParaInput/DarkPhotonSelection_m4l100To170_Nominal/2019-07-17_m4lSR-m4lSB_HZZd-ppZZd_Run2017/
#inputDir=/raid/raid7/lucien/Higgs/DarkZ/ParaInput/DarkPhotonSelection_m4l100To170_Nominal/2019-07-17_m4lSR-m4lSB_HZZd-ppZZd_Run2018/

#outputDir=DataCard/2019-05-10_CutAndCount_m4lSR/
#outputDir=DataCard/2019-05-10_CutAndCount_m4lSR-m4lLowSB-m4lHighSB/
#outputDir=DataCard/2019-05-10_CutAndCount_m4lSR_HZZd/
#outputDir=DataCard/2019-05-10_CutAndCount_m4lSR-m4lSB/
#outputDir=DataCard/2019-05-10_CutAndCount_m4lLowSB-m4lHighSB/
#outputDir=DataCard/2019-05-11_CutAndCount_m4lSR-m4lSB/
#outputDir=DataCard/2019-05-11_CutAndCount_m4lSR_HZZd/
#outputDir=DataCard/2019-05-11_CutAndCount_m4lSR/
#outputDir=DataCard/2019-05-11_CutAndCount_m4lLowSB-m4lHighSB/
#outputDir=DataCard/2019-05-15_CutAndCount_m4lSR-m4lLowSB-m4lHighSB/
#outputDir=DataCard/2019-05-15_CutAndCount_m4lSR-m4lLowSB-m4lHighSB_ppZZd_EspPower2/
#outputDir=DataCard/2019-05-15_CutAndCount_m4lSR-m4lLowSB-m4lHighSB_ppZZd_EspPower4/
#outputDir=DataCard/2019-05-16_CutAndCount_m4lLowSB-m4lHighSB_ppZZd/

#outputDir=DataCard/2019-05-23_CutAndCount_m4lLowSB-m4lHighSB_HZZd-ppZZd_SignalInterpolate/
#outputDir=DataCard/2019-05-23_CutAndCount_m4lSR_HZZd-ppZZd_SignalInterpolate/
#outputDir=DataCard/2019-05-23_CutAndCount_m4lSR-m4lLowSB-m4lHighSB_HZZd-ppZZd_SignalInterpolate/
#outputDir=DataCard/2019-05-23_CutAndCount_m4lSR-m4lLowSB-m4lHighSB_HZZd_SignalInterpolate/
#outputDir=DataCard/2019-06-05_CutAndCount_m4lSR-m4lLowSB-m4lHighSB_HZZd_SignalInterpolate/
#outputDir=DataCard/2019-06-13_CutAndCount_m4lSR-m4lLowSB-m4lHighSB_HZZd_SignalInterpolate_2e/
#outputDir=DataCard/2019-06-13_CutAndCount_m4lSR_HZZd_SignalInterpolate_2e/
#outputDir=DataCard/2019-06-13_CutAndCount_m4lSR_HZZd_SignalInterpolate_2mu/
#outputDir=DataCard/2019-06-13_CutAndCount_m4lLowSB-m4lHighSB_HZZd_SignalInterpolate_2e/
#outputDir=DataCard/2019-06-13_CutAndCount_m4lSR-m4lLowSB-m4lHighSB_HZZd_SignalInterpolate_2mu/
#outputDir=DataCard/2019-06-26_ParametricShape_m4lSR-m4lLowSB-m4lHighSB_HZZd-ppZZd/
#outputDir=DataCard/2019-07-08_ParametricShape_m4lSR-m4lLowSB-m4lHighSB_HZZd-ppZZd/
#outputDir=DataCard/2019-07-08_CutAndCount_m4lSR-m4lLowSB-m4lHighSB_HZZd-ppZZd/
#outputDir=DataCard/2019-07-08_CutAndCount_m4lSR-m4lLowSB-m4lHighSB_HZZd/
#outputDir=DataCard/2019-07-08_ParametricShape_m4lSR-m4lLowSB-m4lHighSB_HZZd/
#outputDir=DataCard/2019-07-08_ParametricShape_m4lSR_HZZd_RunII/
#outputDir=DataCard/2019-07-09_ParametricShape_m4lSR_HZZd_RunII/
#outputDir=DataCard/2019-07-09_CutAndCount_m4lSR_HZZd_Run2016_scaleZX/
#outputDir=DataCard/2019-07-09_CutAndCount_m4lSR_HZZd_Run2016/
outputDir=DataCard/2019-07-17_CutAndCount_m4lSR-m4lLowSB-m4lHighSB_HZZd_Run2016/

# ________________________________________________________________________________________________________________________ ||
#python makeDataCard.py --inputDir ${inputDir} --verbose --outputDir ${outputDir} --sideband --epsilon
#python makeDataCard.py --inputDir ${inputDir} --verbose --outputDir ${outputDir} --sideband --parametric --drawDir /home/lucien/public_html/Higgs/DarkZ/ParametricFit/2019-07-28_ParametricShape_m4lSR-m4lLowSB-m4lHighSB_HZZd-ppZZd/
#python makeParaCard.py --inputDir ${inputDir} --verbose --outputDir ${outputDir} --parametric --drawDir /home/lucien/public_html/Higgs/DarkZ/ParametricFit/2019-06-26_ParametricShape_reference/
python makeDataCard.py --inputDir ${inputDir} --verbose --outputDir ${outputDir} --sideband
#python makeDataCard.py --inputDir ${inputDir} --verbose --outputDir ${outputDir} --parametric --drawDir /home/lucien/public_html/Higgs/DarkZ/ParametricFit/2019-07-09_ParametricShape_m4lSR_HZZd_RunII/

# ________________________________________________________________________________________________________________________ ||
for d in $(ls ${outputDir}); 
do
    python makeWorkspace.py --inputDir ${outputDir}/${d}/ --cardName ${d}.txt --combinePattern "Two*.txt"
done

# ________________________________________________________________________________________________________________________ ||
#python runCombineTask.py --inputDir ${outputDir} --selectStr "Zd_MZD" --option "-t -1 --run=blind --redefineSignalPOIs epsilon --freezeParameters r"
python runCombineTask.py --inputDir ${outputDir} --selectStr "Zd_MZD" --option "-t -1 --run=blind"
#python runCombineTask.py --inputDir ${outputDir} --selectStr "Zd_MZD" --option "-t -1 --run=blind --freezeParameters c0_Higgs_Mu,c1_Higgs_Mu,c2_Higgs_Mu,c3_Higgs_Mu,c4_Higgs_Mu,mean_Mu,width_Mu,alphaL_Mu,alphaR_Mu,nL_Mu,nR_Mu,c0_qqZZ_Mu,c1_qqZZ_Mu,c2_qqZZ_Mu,c3_qqZZ_Mu,c4_qqZZ_Mu,c0_ggZZ_Mu,c1_ggZZ_Mu,c2_ggZZ_Mu,c3_ggZZ_Mu,c4_ggZZ_Mu,meanVar_ZPlusX_Mu,widthVar_ZPlusX,c0_Higgs_El,c1_Higgs_El,c2_Higgs_El,c3_Higgs_El,c4_Higgs_El,mean_El,width_El,alphaL_El,alphaR_El,nL_El,nR_El,c0_qqZZ_El,c1_qqZZ_El,c2_qqZZ_El,c3_qqZZ_El,c4_qqZZ_El,c0_ggZZ_El,c1_ggZZ_El,c2_ggZZ_El,c3_ggZZ_El,c4_ggZZ_El,meanVar_ZPlusX_El,widthVar_ZPlusX,HiggsRate"
#python runCombineTask.py --inputDir ${outputDir} --selectStr "Zd_MZD" --method FitDiagnostics --option "-t -1 --freezeParameters c0_Higgs_Mu,c1_Higgs_Mu,c2_Higgs_Mu,c3_Higgs_Mu,c4_Higgs_Mu,mean_Mu,width_Mu,alphaL_Mu,alphaR_Mu,nL_Mu,nR_Mu,c0_qqZZ_Mu,c1_qqZZ_Mu,c2_qqZZ_Mu,c3_qqZZ_Mu,c4_qqZZ_Mu,c0_ggZZ_Mu,c1_ggZZ_Mu,c2_ggZZ_Mu,c3_ggZZ_Mu,c4_ggZZ_Mu,meanVar_ZPlusX_Mu,widthVar_ZPlusX,c0_Higgs_El,c1_Higgs_El,c2_Higgs_El,c3_Higgs_El,c4_Higgs_El,mean_El,width_El,alphaL_El,alphaR_El,nL_El,nR_El,c0_qqZZ_El,c1_qqZZ_El,c2_qqZZ_El,c3_qqZZ_El,c4_qqZZ_El,c0_ggZZ_El,c1_ggZZ_El,c2_ggZZ_El,c3_ggZZ_El,c4_ggZZ_El,widthVar_ZPlusX_El,widthVar_ZPlusX_Mu,meanVar_ZPlusX_El,meanVar_ZPlusX_Mu,HiggsRate"
