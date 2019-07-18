#!/bin/bash

# ________________________________________________________________________________________________________________________ ||
inputDir2016=/raid/raid7/lucien/Higgs/HToZdZd/DarkPhotonSR/StatInput/2019-07-18_Run2016/
inputDir2017=/raid/raid7/lucien/Higgs/HToZdZd/DarkPhotonSR/StatInput/2019-07-18_Run2017/
inputDir2018=/raid/raid7/lucien/Higgs/HToZdZd/DarkPhotonSR/StatInput/2019-07-18_Run2018/
outputDir=HToZdZd_DataCard/2019-07-18_RunII/

# ________________________________________________________________________________________________________________________ ||
python makeHToZdZdCard.py --inputDir ${inputDir2016} --verbose --outputDir ${outputDir} --appendToPath "2016" --systTextFile Config/Syst_Run2016.txt,Config/Syst_2mu2e_Run2016.txt
python makeHToZdZdCard.py --inputDir ${inputDir2017} --verbose --outputDir ${outputDir} --appendToPath "2017" --systTextFile Config/Syst_Run2017.txt,Config/Syst_2mu2e_Run2017.txt
python makeHToZdZdCard.py --inputDir ${inputDir2018} --verbose --outputDir ${outputDir} --appendToPath "2018" --systTextFile Config/Syst_Run2018.txt,Config/Syst_2mu2e_Run2018.txt

# ________________________________________________________________________________________________________________________ ||
for d in $(ls ${outputDir}); 
do
    python makeWorkspace.py --inputDir ${outputDir}/${d}/ --cardName ${d}.txt --combinePattern "Zd*.txt"
done

## ________________________________________________________________________________________________________________________ ||
python runCombineTask.py --inputDir ${outputDir} --selectStr "Zd_MZD" --option "-t -1 --run=blind"
