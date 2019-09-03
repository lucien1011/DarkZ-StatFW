#!/bin/bash

# ________________________________________________________________________________________________________________________ ||
mkDC=true
mkWS=true
mkLimit=true
mkFit=true

# ________________________________________________________________________________________________________________________ ||
inputDir2016=/raid/raid7/lucien/Higgs/HToZdZd/DarkPhotonSR/StatInput/2019-08-21_Run2016/
inputDir2017=/raid/raid7/lucien/Higgs/HToZdZd/DarkPhotonSR/StatInput/2019-08-21_Run2017/
inputDir2018=/raid/raid7/lucien/Higgs/HToZdZd/DarkPhotonSR/StatInput/2019-08-21_Run2018/
#outputDir=HToZdZd_DataCard/2019-08-21_RunII/
outputDir=HToZdZd_DataCard/2019-09-03_RunII/

#systTextFile2016=Config/Syst_Run2016.txt,Config/Syst_MuMu_Run2016.txt,Config/Syst_ElMu_Run2016.txt,Config/Syst_ElEl_Run2016.txt,Config/Syst_MuEl_Run2016.txt
#systTextFile2017=Config/Syst_Run2017.txt,Config/Syst_MuMu_Run2017.txt,Config/Syst_ElMu_Run2017.txt,Config/Syst_ElEl_Run2017.txt,Config/Syst_MuEl_Run2017.txt
#systTextFile2018=Config/Syst_Run2018.txt,Config/Syst_MuMu_Run2018.txt,Config/Syst_ElMu_Run2018.txt,Config/Syst_ElEl_Run2018.txt,Config/Syst_MuEl_Run2018.txt

systTextFile2016=Config/Syst_Run2016.txt,Config/Syst_MuMu_Run2016.txt,Config/Syst_ElEl_Run2016.txt
systTextFile2017=Config/Syst_Run2017.txt,Config/Syst_MuMu_Run2017.txt,Config/Syst_ElEl_Run2017.txt
systTextFile2018=Config/Syst_Run2018.txt,Config/Syst_MuMu_Run2018.txt,Config/Syst_ElEl_Run2018.txt

zxShapeDir2016=/raid/raid7/lucien/Higgs/HToZdZd/DarkPhotonSR/StatInput/2019-08-21_Run2016/
zxShapeDir2017=/raid/raid7/lucien/Higgs/HToZdZd/DarkPhotonSR/StatInput/2019-08-21_Run2017/
zxShapeDir2018=/raid/raid7/lucien/Higgs/HToZdZd/DarkPhotonSR/StatInput/2019-08-21_Run2018/

interDir2016=/home/lucien/public_html/Higgs/HToZdZd/Interpolation/2019-08-21_Run2016/
interDir2017=/home/lucien/public_html/Higgs/HToZdZd/Interpolation/2019-08-21_Run2017/
interDir2018=/home/lucien/public_html/Higgs/HToZdZd/Interpolation/2019-08-21_Run2018/

postFitPlotDir=/home/lucien/public_html/Higgs/HToZdZd/FitDiagnostics/2019-09-03_RunII/

# ________________________________________________________________________________________________________________________ ||
if ${mkDC} ; then
    python makeHToZdZdCard.py --inputDir ${inputDir2016} --verbose --outputDir ${outputDir} --appendToPath "2016" --systTextFile ${systTextFile2016} --interpolPath ${interDir2016} --zxShapeDir ${zxShapeDir2016} 
    python makeHToZdZdCard.py --inputDir ${inputDir2017} --verbose --outputDir ${outputDir} --appendToPath "2017" --systTextFile ${systTextFile2017} --interpolPath ${interDir2017} --zxShapeDir ${zxShapeDir2017} 
    python makeHToZdZdCard.py --inputDir ${inputDir2018} --verbose --outputDir ${outputDir} --appendToPath "2018" --systTextFile ${systTextFile2018} --interpolPath ${interDir2018} --zxShapeDir ${zxShapeDir2018} 
fi

## ________________________________________________________________________________________________________________________ ||
if ${mkWS} ; then
    for d in $(ls ${outputDir}); 
    do
        python makeWorkspace.py --inputDir ${outputDir}/${d}/ --cardName ${d}.txt --combinePattern "Zd*.txt"
    done
fi

# ________________________________________________________________________________________________________________________ ||
if ${mkLimit} ; then
    #python runCombineTask.py --inputDir ${outputDir} --selectStr "Zd_MZD" --option "-t -1 --run=blind"
    python runCombineTask.py --inputDir ${outputDir} --selectStr "Zd_MZD"
fi

# ________________________________________________________________________________________________________________________ ||
if ${mkFit} ; then
    for m in 4.04 7.20517492369 12.0433938681 15.5316658805 18.0384780411 20.4339081063 25.0703252313 30.0011699553 34.4975235989 40.0654267675 45.1601374688 55.1312355409 60.0096060023;
    do
        python runCombineTask.py --inputDir ${outputDir} --selectStr "Zd_MZD${m}" --option "" --method FitDiagnostics
        python PlotScript/plotNuisance.py --inputPath ${outputDir}/Zd_MZD${m}/fitDiagnostics.root --outputPath ${postFitPlotDir}/Zd_MZD${m}.pdf
    done
fi
