#!/bin/bash

# ________________________________________________________________________________________________________________________ ||
mkDC=true
mkWS=true
mkLimit=true
mkToyLimit=false
mkSignif=false
mkFit=false
mkImpact=false

# ________________________________________________________________________________________________________________________ ||
inputDir2016=/raid/raid7/lucien/Higgs/HToZdZd/DarkPhotonSR/StatInput/2020-02-29_SR2D_Run2016/
inputDir2017=/raid/raid7/lucien/Higgs/HToZdZd/DarkPhotonSR/StatInput/2020-02-29_SR2D_Run2017/
inputDir2018=/raid/raid7/lucien/Higgs/HToZdZd/DarkPhotonSR/StatInput/2020-02-29_SR2D_Run2018/

systTextFile2016=Config/Syst_Run2016.txt,Config/Syst_MuMu_Run2016.txt,Config/Syst_ElMu_Run2016.txt,Config/Syst_ElEl_Run2016.txt,Config/Syst_MuEl_Run2016.txt
systTextFile2017=Config/Syst_Run2017.txt,Config/Syst_MuMu_Run2017.txt,Config/Syst_ElMu_Run2017.txt,Config/Syst_ElEl_Run2017.txt,Config/Syst_MuEl_Run2017.txt
systTextFile2018=Config/Syst_Run2018.txt,Config/Syst_MuMu_Run2018.txt,Config/Syst_ElMu_Run2018.txt,Config/Syst_ElEl_Run2018.txt,Config/Syst_MuEl_Run2018.txt

zxShapeDir2016=/raid/raid7/lucien/Higgs/HToZdZd/DarkPhotonSR/StatInput/2020-02-29_SR2D_Run2016/
zxShapeDir2017=/raid/raid7/lucien/Higgs/HToZdZd/DarkPhotonSR/StatInput/2020-02-29_SR2D_Run2017/
zxShapeDir2018=/raid/raid7/lucien/Higgs/HToZdZd/DarkPhotonSR/StatInput/2020-02-29_SR2D_Run2018/

interDir2016=/home/lucien/public_html/Higgs/HToZdZd/Interpolation/2020-02-29_SignalInterpolation2D_Run2016/
interDir2017=/home/lucien/public_html/Higgs/HToZdZd/Interpolation/2020-02-29_SignalInterpolation2D_Run2017/
interDir2018=/home/lucien/public_html/Higgs/HToZdZd/Interpolation/2020-02-29_SignalInterpolation2D_Run2018/

postFitPlotDir=/home/lucien/public_html/Higgs/HToZdZd/FitDiagnostics/2019-09-03_RunII/
impactPlotDir=/home/lucien/public_html/Higgs/HToZdZd/Impacts/2019-09-03_RunII/

#outputDir=HToZdZd_DataCard/2020-03-03_SR2D_RunII_Mu/
#outputDir=HToZdZd_DataCard/2020-03-15_SR2D_RunII_Mu/
outputDir=HToZdZd_DataCard/2020-03-17_SR2D_RunII_Mu/

#taskName=2020-03-06_SR2D_RunII_Mu
taskName=2020-03-06_SR2D_RunII_Mu

# ________________________________________________________________________________________________________________________ ||
if ${mkDC} ; then
    python makeHToZdZd2DCard.py --inputDir ${inputDir2016} --verbose --outputDir ${outputDir} --appendToPath "2016" --systTextFile ${systTextFile2016} --zxShapeDir ${zxShapeDir2016} --interpolPath ${interDir2016} --muOnly 
    python makeHToZdZd2DCard.py --inputDir ${inputDir2017} --verbose --outputDir ${outputDir} --appendToPath "2017" --systTextFile ${systTextFile2017} --zxShapeDir ${zxShapeDir2017} --interpolPath ${interDir2017} --muOnly
    python makeHToZdZd2DCard.py --inputDir ${inputDir2018} --verbose --outputDir ${outputDir} --appendToPath "2018" --systTextFile ${systTextFile2018} --zxShapeDir ${zxShapeDir2018} --interpolPath ${interDir2018} --muOnly
fi

## ________________________________________________________________________________________________________________________ ||
if ${mkWS} ; then
    for d in $(ls ${outputDir}); 
    do
        python makeWorkspace.py --inputDir ${outputDir}/${d}/ --cardName ${d}.txt --combinePattern "Zd*_201*.txt"
    done
fi

# ________________________________________________________________________________________________________________________ ||
if ${mkLimit} ; then
    #python runCombineTask.py --inputDir ${outputDir} --selectStr "Zd_MZD" --option "-t -1 --run=blind"
    python runCombineTask.py --inputDir ${outputDir} --selectStr "Zd_MZD" --run_in_wsdir
fi

# ________________________________________________________________________________________________________________________ ||
if ${mkToyLimit} ; then
    python runToyLimit.py --inputDir ${outputDir} --selectStr "Zd_MZD*" --option "" --method HybridNew --option "--LHCmode LHC-limits" --crab --taskName ${taskName}
fi

# ________________________________________________________________________________________________________________________ ||
if ${mkSignif} ; then
    python runCombineTask.py --inputDir ${outputDir} --selectStr "Zd_MZD" --option "" --method Significance
fi

# ________________________________________________________________________________________________________________________ ||
if ${mkFit} ; then
    for m in 4.04 7.20517492369 12.0433938681 15.5316658805 18.0384780411 20.4339081063 25.0703252313 30.0011699553 34.4975235989 40.0654267675 45.1601374688 55.1312355409 60.0096060023;
    do
        python runCombineTask.py --inputDir ${outputDir} --selectStr "Zd_MZD${m}" --option "" --method FitDiagnostics
        python PlotScript/plotNuisance.py --inputPath ${outputDir}/Zd_MZD${m}/fitDiagnostics.root --outputPath ${postFitPlotDir}/Zd_MZD${m}.pdf
    done
fi

# ________________________________________________________________________________________________________________________ ||
if ${mkImpact} ; then
    #for m in 4.04 7.20517492369 12.0433938681 15.5316658805 18.0384780411 20.4339081063 25.0703252313 30.0011699553 34.4975235989 40.0654267675 45.1601374688 55.1312355409 60.0096060023;
    #for m in 10.9545291766;
    for m in $(ls ${outputDir}) ;
    do
        #python runCombineTask.py --inputDir ${outputDir} --selectStr "Zd_MZD${m}" --method Impacts 
        #plotImpacts.py -i ${outputDir}/Zd_MZD${m}/impacts.json -o ${impactPlotDir}/Zd_MZD${m}
        if [[ ${m} == *"D19."* ]] ; then 
            python runCombineTask.py --inputDir ${outputDir} --selectStr "${m}" --method Impacts ;
            plotImpacts.py -i ${outputDir}/${m}/impacts.json -o ${impactPlotDir}/${m} ;
        fi
    done
fi
