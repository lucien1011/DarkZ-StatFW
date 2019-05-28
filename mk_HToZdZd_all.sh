#!/bin/bash

inputDir=/raid/raid7/lucien/Higgs/HToZdZd/DarkPhotonSR/StatInput/2019-05-28_136p1_RunII_RatioCut0p05/
outputDir=HToZdZd_DataCard/2019-05-28_CutAndCount_RunII_RatioCut0p05/

python makeHToZdZdCard.py --inputDir ${inputDir} --verbose --outputDir ${outputDir} 

for d in $(ls ${outputDir}); 
do
    python makeWorkspace.py --inputDir ${outputDir}/${d}/ --pattern "Zd_MZD*.txt"
done

#python runCombineTask.py --inputDir ${outputDir} --selectStr "Zd_MZD" --option "-t -1 --run=blind --redefineSignalPOIs kappa --freezeParameters r"
python runCombineTask.py --inputDir ${outputDir} --selectStr "Zd_MZD" --option "-t -1 --run=blind"
python runCombineTask.py --inputDir ${outputDir} --selectStr "Zd_MZD" --option "-t -1 --expectSignal=1" --method=Significance
