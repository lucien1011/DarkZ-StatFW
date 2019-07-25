#!/bin/bash

# ________________________________________________________________________________________________________________________ ||
inputDir2016=/raid/raid7/lucien/Higgs/DarkZ/ParaInput/DarkPhotonSelection_m4l100To170_Nominal/2019-07-17_m4lSR-m4lSB_HZZd-ppZZd_Run2016/
inputDir2017=/raid/raid7/lucien/Higgs/DarkZ/ParaInput/DarkPhotonSelection_m4l100To170_Nominal/2019-07-17_m4lSR-m4lSB_HZZd-ppZZd_Run2017/
inputDir2018=/raid/raid7/lucien/Higgs/DarkZ/ParaInput/DarkPhotonSelection_m4l100To170_Nominal/2019-07-17_m4lSR-m4lSB_HZZd-ppZZd_Run2018/

interDir2016=/home/lucien/public_html/Higgs/DarkZ/Interpolation/2019-07-17_m4lSR-m4lSB_HZZd-ppZZd_Run2016/
interDir2017=/home/lucien/public_html/Higgs/DarkZ/Interpolation/2019-07-17_m4lSR-m4lSB_HZZd-ppZZd_Run2017/
interDir2018=/home/lucien/public_html/Higgs/DarkZ/Interpolation/2019-07-17_m4lSR-m4lSB_HZZd-ppZZd_Run2018/

#outputDir=DataCard/2019-07-17_CutAndCount_m4lSR-m4lLowSB-m4lHighSB_HZZd_RunII/
outputDir=DataCard/2019-07-24_CutAndCount_m4lSR-m4lLowSB-m4lHighSB_HZZd-ppZZd_RunII/
#outputDir=DataCard/2019-07-17_CutAndCount_m4lSR-m4lLowSB-m4lHighSB_HZZd-ppZZd_RunII_EpsPOI/

# ________________________________________________________________________________________________________________________ ||
python makeDataCard.py --inputDir ${inputDir2016} --verbose --outputDir ${outputDir} --sideband --appendToPath "2016" --systTextFile Config/Syst_Run2016.txt,Config/Syst_2mu_Run2016.txt,Config/Syst_2e_Run2016.txt --interpolPath ${interDir2016} --setDataCountToMC #--epsilon
python makeDataCard.py --inputDir ${inputDir2017} --verbose --outputDir ${outputDir} --sideband --appendToPath "2017" --systTextFile Config/Syst_Run2017.txt,Config/Syst_2mu_Run2017.txt,Config/Syst_2e_Run2017.txt --interpolPath ${interDir2017} --setDataCountToMC #--epsilon
python makeDataCard.py --inputDir ${inputDir2018} --verbose --outputDir ${outputDir} --sideband --appendToPath "2018" --systTextFile Config/Syst_Run2018.txt,Config/Syst_2mu_Run2018.txt,Config/Syst_2e_Run2018.txt --interpolPath ${interDir2018} --setDataCountToMC #--epsilon
#
## ________________________________________________________________________________________________________________________ ||
for d in $(ls ${outputDir}); 
do
    python makeWorkspace.py --inputDir ${outputDir}/${d}/ --cardName ${d}.txt --combinePattern "Two*.txt"
done

# ________________________________________________________________________________________________________________________ ||
python runCombineTask.py --inputDir ${outputDir} --selectStr "Zd_MZD" --option "-t -1 --run=blind"
#python runCombineTask.py --inputDir ${outputDir} --selectStr "Zd_MZD" --option "-t -1 --run=blind --redefineSignalPOIs epsilon --freezeParameters r"
