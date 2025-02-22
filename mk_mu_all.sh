#!/bin/bash

# ________________________________________________________________________________________________________________________ ||
mkDC=false
mkWS=false
mkAsymLimit=true
mkToyLimit=false
mkSignif=false
mkFit=false
mkImpact=false

# ________________________________________________________________________________________________________________________ ||
inputDir2016=/raid/raid7/lucien/Higgs/DarkZ/ParaInput/DarkPhotonSelection_m4l100To170_Nominal/2019-12-02_m4lSR-m4lSB_HZZd-Run2016/
inputDir2017=/raid/raid7/lucien/Higgs/DarkZ/ParaInput/DarkPhotonSelection_m4l100To170_Nominal/2019-12-02_m4lSR-m4lSB_HZZd-Run2017/
inputDir2018=/raid/raid7/lucien/Higgs/DarkZ/ParaInput/DarkPhotonSelection_m4l100To170_Nominal/2019-12-02_m4lSR-m4lSB_HZZd-Run2018/

interDir2016=/home/lucien/public_html/Higgs/DarkZ/Interpolation/2019-12-04_m4lSR-m4lSB_HZZd_SignalInterpolation_Run2016/
interDir2017=/home/lucien/public_html/Higgs/DarkZ/Interpolation/2019-12-04_m4lSR-m4lSB_HZZd_SignalInterpolation_Run2017/
interDir2018=/home/lucien/public_html/Higgs/DarkZ/Interpolation/2019-12-04_m4lSR-m4lSB_HZZd_SignalInterpolation_Run2018/

zxShapeDir2016=/raid/raid7/lucien/Higgs/DarkZ/ParaInput/DarkPhotonSelection_m4l100To170_Nominal/2019-12-02_m4lSR-m4lSB_HZZd-Run2016/
zxShapeDir2017=/raid/raid7/lucien/Higgs/DarkZ/ParaInput/DarkPhotonSelection_m4l100To170_Nominal/2019-12-02_m4lSR-m4lSB_HZZd-Run2017/
zxShapeDir2018=/raid/raid7/lucien/Higgs/DarkZ/ParaInput/DarkPhotonSelection_m4l100To170_Nominal/2019-12-02_m4lSR-m4lSB_HZZd-Run2018/

sigSF=1.

outputDir=DataCard/2020-03-03_CutAndCount_m4lSR-HZZd_RunII_Mu/

systTextFile2016=Config/Syst_Run2016.txt,Config/Syst_MuMu_Run2016.txt,Config/Syst_ElMu_Run2016.txt,Config/Syst_ElEl_Run2016.txt,Config/Syst_MuEl_Run2016.txt
systTextFile2017=Config/Syst_Run2017.txt,Config/Syst_MuMu_Run2017.txt,Config/Syst_ElMu_Run2017.txt,Config/Syst_ElEl_Run2017.txt,Config/Syst_MuEl_Run2017.txt
systTextFile2018=Config/Syst_Run2018.txt,Config/Syst_MuMu_Run2018.txt,Config/Syst_ElMu_Run2018.txt,Config/Syst_ElEl_Run2018.txt,Config/Syst_MuEl_Run2018.txt

postFitPlotDir=/home/lucien/public_html/Higgs/DarkZ/StatFW/2019-09-02_CutAndCount_m4lSR-m4lLowSB-m4lHighSB_HZZd_RunII/FitDiagnostics/
impactPlotDir=/home/lucien/public_html/Higgs/DarkZ/StatFW/2019-09-02_CutAndCount_m4lSR-m4lLowSB-m4lHighSB_HZZd_RunII/Impacts/

# ________________________________________________________________________________________________________________________ ||
if ${mkDC} ; then
    python makeDataCard.py --inputDir ${inputDir2016} --verbose --outputDir ${outputDir} --sideband --appendToPath "2016" --systTextFile ${systTextFile2016} --zxShapeDir ${zxShapeDir2016} --interpolPath ${interDir2016} --sigSF=${sigSF} --muOnly  
    python makeDataCard.py --inputDir ${inputDir2017} --verbose --outputDir ${outputDir} --sideband --appendToPath "2017" --systTextFile ${systTextFile2017} --zxShapeDir ${zxShapeDir2017} --interpolPath ${interDir2017} --sigSF=${sigSF} --muOnly  
    python makeDataCard.py --inputDir ${inputDir2018} --verbose --outputDir ${outputDir} --sideband --appendToPath "2018" --systTextFile ${systTextFile2018} --zxShapeDir ${zxShapeDir2018} --interpolPath ${interDir2018} --sigSF=${sigSF} --muOnly  
fi

# ________________________________________________________________________________________________________________________ ||
if ${mkWS} ; then
    for d in $(ls ${outputDir}); 
    do
        #echo ${d} ;
        python makeWorkspace.py --inputDir ${outputDir}/${d}/ --cardName ${d}.txt --combinePattern "*_S*.txt" ;
    done
fi

# ________________________________________________________________________________________________________________________ ||
if ${mkAsymLimit} ; then
    #python runCombineTask.py --inputDir ${outputDir} --selectStr "Zd_MZD" --option "-t -1 --run=blind"
    python runCombineTask.py --inputDir ${outputDir} --selectStr "Zd_MZD" --option "" --run_in_wsdir
    #python runCombineTask.py --inputDir ${outputDir} --selectStr "Zd_MZD" --option "-t -1 --run=blind --redefineSignalPOIs epsilon --freezeParameters r"
fi

# ________________________________________________________________________________________________________________________ ||
if ${mkToyLimit} ; then
    python runCombineTask.py --inputDir ${outputDir} --selectStr "Zd_MZD" --option "" --method HybridNew --option "--LHEmode LHE-limits"
fi

# ________________________________________________________________________________________________________________________ ||
if ${mkSignif} ; then
    python runCombineTask.py --inputDir ${outputDir} --selectStr "Zd_MZD" --option "" --method Significance
fi

# ________________________________________________________________________________________________________________________ ||
if ${mkFit} ; then
    for m in 4.04 7.20517492369 12.0433938681 15.5316658805 18.0384780411 20.4339081063 25.0703252313 30.0011699553 34.4975235989 ;
    #for m in 17.4195711821 ;
    do
        python runCombineTask.py --inputDir ${outputDir} --selectStr "Zd_MZD${m}" --option "" --method FitDiagnostics
        python PlotScript/plotNuisance.py --inputPath ${outputDir}/Zd_MZD${m}/fitDiagnostics.root --outputPath ${postFitPlotDir}/Zd_MZD${m}.pdf
    done
fi

# ________________________________________________________________________________________________________________________ ||
if ${mkImpact} ; then
    mkdir ${impactPlotDir} ;
    #for m in 4.04 7.20517492369 12.0433938681 15.5316658805 18.0384780411 20.4339081063 25.0703252313 30.0011699553 34.4975235989;
    for m in 4.04 7.20517492369 12.0433938681 15.5316658805 18.0384780411 20.4339081063 25.0703252313 30.0011699553 34.4975235989;
    #for m in $(ls ${outputDir}) ;
    do      
        python runCombineTask.py --inputDir ${outputDir} --selectStr "Zd_MZD${m}" --method Impacts ;
        plotImpacts.py -i ${outputDir}/Zd_MZD${m}/impacts.json -o ${impactPlotDir}/Zd_MZD${m} ;
        #if [[ ${m} == *"D33."* ]] ; then 
        #    python runCombineTask.py --inputDir ${outputDir} --selectStr "${m}" --method Impacts ;
        #    plotImpacts.py -i ${outputDir}/${m}/impacts.json -o ${impactPlotDir}/${m} ;
        #fi
    done
fi
