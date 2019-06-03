#!/bin/bash

#inputDir=/raid/raid7/lucien/Higgs/HToZdZd/DarkPhotonSR/StatInput/2019-03-29_136p1_RatioCut0p05/
#inputDir=/raid/raid7/lucien/Higgs/HToZdZd/DarkPhotonSR/StatInput/2019-05-27_136p1_RatioCut0p05/
inputDir=/raid/raid7/lucien/Higgs/HToZdZd/DarkPhotonSR/StatInput/2019-05-28_136p1_RunII_OptimiseMassRatio/

for w in 0.01 0.02 0.03 0.04 0.05 0.06 0.07 0.08 0.09 ;
do
    #outputDir=HToZdZd_DataCard/2019-05-28_CutAndCount_RunII_RatioOptimisation/${w}/
    #outputDir=HToZdZd_DataCard/2019-05-28_CutAndCount_RunII_RatioOptimisation_OnlyMu/${w}/
    outputDir=HToZdZd_DataCard/2019-05-28_CutAndCount_RunII_RatioOptimisation_OnlyEl/${w}/
    python makeHToZdZdCard.py --inputDir ${inputDir} --verbose --outputDir ${outputDir} --massRatio=${w}
    for d in $(ls ${outputDir}); 
    do
        python makeWorkspace.py --inputDir ${outputDir}/${d}/ --pattern "Zd_MZD*.txt"
    done
    python runCombineTask.py --inputDir ${outputDir} --selectStr "Zd_MZD" --option "-t -1 --run=blind"
    python runCombineTask.py --inputDir ${outputDir} --selectStr "Zd_MZD" --option "-t -1 --expectSignal=1" --method=Significance
done
