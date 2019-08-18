#!/bin/bash

# ________________________________________________________________________________________________________________________ ||
inputDir2016=/raid/raid7/lucien/Higgs/DarkZ/ParaInput/DarkPhotonSelection_m4l100To170_Nominal/2019-08-14_m4lSR-m4lSB_HZZd-ppZZd_Run2016/
inputDir2017=/raid/raid7/lucien/Higgs/DarkZ/ParaInput/DarkPhotonSelection_m4l100To170_Nominal/2019-08-14_m4lSR-m4lSB_HZZd-ppZZd_Run2017/
inputDir2018=/raid/raid7/lucien/Higgs/DarkZ/ParaInput/DarkPhotonSelection_m4l100To170_Nominal/2019-08-14_m4lSR-m4lSB_HZZd-ppZZd_Run2018/

interDir2016=/home/lucien/public_html/Higgs/DarkZ/Interpolation/2019-08-14_m4lSR-m4lSB_HZZd-ppZZd_Run2016/
interDir2017=/home/lucien/public_html/Higgs/DarkZ/Interpolation/2019-08-14_m4lSR-m4lSB_HZZd-ppZZd_Run2017/
interDir2018=/home/lucien/public_html/Higgs/DarkZ/Interpolation/2019-08-14_m4lSR-m4lSB_HZZd-ppZZd_Run2018/

zxShapeDir2016=/raid/raid7/lucien/Higgs/DarkZ/ParaInput/DarkPhotonSelection_m4l100To170_Nominal/2019-08-14_m4lSR-m4lSB_HZZd-ppZZd_Run2016/
zxShapeDir2017=/raid/raid7/lucien/Higgs/DarkZ/ParaInput/DarkPhotonSelection_m4l100To170_Nominal/2019-08-14_m4lSR-m4lSB_HZZd-ppZZd_Run2017/
zxShapeDir2018=/raid/raid7/lucien/Higgs/DarkZ/ParaInput/DarkPhotonSelection_m4l100To170_Nominal/2019-08-14_m4lSR-m4lSB_HZZd-ppZZd_Run2018/

#outputDir=DataCard/2019-07-17_CutAndCount_m4lSR-m4lLowSB-m4lHighSB_HZZd_RunII/
#outputDir=DataCard/2019-07-24_CutAndCount_m4lSR-m4lLowSB-m4lHighSB_HZZd-ppZZd_RunII/
#outputDir=DataCard/2019-07-17_CutAndCount_m4lSR-m4lLowSB-m4lHighSB_HZZd-ppZZd_RunII_EpsPOI/
#outputDir=DataCard/2019-08-01_CutAndCount_m4lSR-m4lLowSB-m4lHighSB_HZZd-ppZZd_RunII/
#outputDir=DataCard/2019-08-02_CutAndCount_m4lSR-m4lLowSB-m4lHighSB_HZZd-ppZZd_RunII/
#outputDir=DataCard/2019-08-02_CutAndCount_m4lSR-m4lLowSB-m4lHighSB_HZZd_RunII/
#outputDir=DataCard/2019-08-05_CutAndCount_m4lSR-m4lLowSB-m4lHighSB_HZZd_RunII/
#outputDir=DataCard/2019-08-16_CutAndCount_m4lSR-m4lLowSB-m4lHighSB_HZZd_RunII/
outputDir=DataCard/2019-08-16_CutAndCount_m4lSR-m4lLowSB-m4lHighSB_HZZd_RunII/

systTextFile2016=Config/Syst_Run2016.txt,Config/Syst_MuMu_Run2016.txt,Config/Syst_ElMu_Run2016.txt,Config/Syst_ElEl_Run2016.txt,Config/Syst_MuEl_Run2016.txt
systTextFile2017=Config/Syst_Run2017.txt,Config/Syst_MuMu_Run2017.txt,Config/Syst_ElMu_Run2017.txt,Config/Syst_ElEl_Run2017.txt,Config/Syst_MuEl_Run2017.txt
systTextFile2018=Config/Syst_Run2018.txt,Config/Syst_MuMu_Run2018.txt,Config/Syst_ElMu_Run2018.txt,Config/Syst_ElEl_Run2018.txt,Config/Syst_MuEl_Run2018.txt

# ________________________________________________________________________________________________________________________ ||
python makeDataCard.py --inputDir ${inputDir2016} --verbose --outputDir ${outputDir} --sideband --appendToPath "2016" --systTextFile ${systTextFile2016} --setDataCountToMC --zxShapeDir ${zxShapeDir2016} --interpolPath ${interDir2016} #--epsilon  
python makeDataCard.py --inputDir ${inputDir2017} --verbose --outputDir ${outputDir} --sideband --appendToPath "2017" --systTextFile ${systTextFile2017} --setDataCountToMC --zxShapeDir ${zxShapeDir2017} --interpolPath ${interDir2017} #--epsilon  
python makeDataCard.py --inputDir ${inputDir2018} --verbose --outputDir ${outputDir} --sideband --appendToPath "2018" --systTextFile ${systTextFile2018} --setDataCountToMC --zxShapeDir ${zxShapeDir2018} --interpolPath ${interDir2018} #--epsilon  
#
## ________________________________________________________________________________________________________________________ ||
for d in $(ls ${outputDir}); 
do
    #echo ${d} ;
    python makeWorkspace.py --inputDir ${outputDir}/${d}/ --cardName ${d}.txt --combinePattern "*_S*.txt" ;
done

# ________________________________________________________________________________________________________________________ ||
python runCombineTask.py --inputDir ${outputDir} --selectStr "Zd_MZD" --option "-t -1 --run=blind"
#python runCombineTask.py --inputDir ${outputDir} --selectStr "Zd_MZD" --option "-t -1 --run=blind --redefineSignalPOIs epsilon --freezeParameters r"
