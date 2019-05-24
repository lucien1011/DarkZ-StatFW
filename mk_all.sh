#!/bin/bash

#inputDir=/raid/raid7/lucien/Higgs/DarkZ/ParaInput/DarkPhotonSelection_m4l100To170_Nominal/2019-05-09_m4lSR-m4lLowSB-m4lHighSB_HZZd-ppZZd/
#inputDir=/raid/raid7/lucien/Higgs/DarkZ/ParaInput/DarkPhotonSelection_m4l100To170_Nominal/2019-05-09_m4lSR-m4lSB_HZZd-ppZZd/
inputDir=/raid/raid7//lucien/Higgs/DarkZ/ParaInput/DarkPhotonSelection_m4l100To170_Nominal/2019-05-15_m4lSR-m4lSB_HZZd-ppZZd/
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
outputDir=DataCard/2019-05-23_CutAndCount_m4lSR-m4lLowSB-m4lHighSB_HZZd_SignalInterpolate/

#python makeDataCardV2.py --inputDir ${inputDir} --verbose --outputDir ${outputDir} --sideband --epsilon
#python makeDataCardV2.py --inputDir ${inputDir} --verbose --outputDir ${outputDir} --sideband
#
#for d in $(ls ${outputDir}); 
#do
#    python makeWorkspace.py --inputDir ${outputDir}/${d}/ --pattern "Zd_MZD*.txt"
#done

#python runCombineTask.py --inputDir ${outputDir} --selectStr "Zd_MZD" --option "-t -1 --run=blind --redefineSignalPOIs epsilon --freezeParameters r"
python runCombineTask.py --inputDir ${outputDir} --selectStr "Zd_MZD" --option "-t -1 --run=blind"
