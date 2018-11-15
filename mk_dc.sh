#!/bin/bash

#python makeDataCard.py --inputDir /raid/raid7/lucien/Higgs/DarkZ/StatInput/DarkPhotonSelection_m4l118To130_Nominal/2018-10-21_DarkPhotonSR-Unblinding/ --outputDir DataCard/2018-10-23_Unblinding/
#python makeDataCard.py --inputDir /raid/raid7/lucien/Higgs/DarkZ/StatInput/DarkPhotonSelection_m4l118To130_Nominal/2018-10-24_DarkPhotonSR-Unblinding/ --outputDir DataCard/2018-10-24_Unblinding/
#python makeDataCard.py --inputDir /raid/raid7/lucien/Higgs/DarkZ/StatInput/DarkPhotonSelection_m4l118To130_Nominal/2018-10-25_DarkPhotonSR-Unblinding/ --outputDir DataCard/2018-10-25_Unblinding/
#python makeDataCard.py --inputDir /raid/raid7/lucien/Higgs/DarkZ/StatInput/DarkPhotonSelection_m4l118To130_Nominal/2018-10-25_DarkPhotonSR-Unblinding/ --outputDir DataCard/2018-10-25_35p9_Unblinding/
#python makeDataCard.py --inputDir /raid/raid7/lucien/Higgs/DarkZ/StatInput/DarkPhotonSelection_m4l118To130_Nominal/2018-11-09_DarkPhotonSR-150fb-Unblinding/ --outputDir DataCard/2018-11-09_150p0_Unblinding/

python makeDataCardV2.py --inputDir /raid/raid7/lucien/Higgs/DarkZ/ParaInput/DarkPhotonSelection_m4l118To130_Nominal/2018-11-15_DarkPhotonSR-Unblinding/ --outputDir DataCard/2018-11-15_150p0_Unblinding_NoSB/ --verbose
python makeDataCardV2.py --inputDir /raid/raid7/lucien/Higgs/DarkZ/ParaInput/DarkPhotonSelection_m4l118To130_Nominal/2018-11-15_DarkPhotonSR-Unblinding/ --outputDir DataCard/2018-11-15_150p0_Unblinding/ --verbose --sideband
