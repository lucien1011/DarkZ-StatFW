#!/bin/bash

#python makeDataCard.py --inputDir /raid/raid7/lucien/Higgs/DarkZ/StatInput/DarkPhotonSelection_m4l118To130_Nominal/2018-10-21_DarkPhotonSR-Unblinding/ --outputDir DataCard/2018-10-23_Unblinding/
#python makeDataCard.py --inputDir /raid/raid7/lucien/Higgs/DarkZ/StatInput/DarkPhotonSelection_m4l118To130_Nominal/2018-10-24_DarkPhotonSR-Unblinding/ --outputDir DataCard/2018-10-24_Unblinding/
#python makeDataCard.py --inputDir /raid/raid7/lucien/Higgs/DarkZ/StatInput/DarkPhotonSelection_m4l118To130_Nominal/2018-10-25_DarkPhotonSR-Unblinding/ --outputDir DataCard/2018-10-25_Unblinding/
#python makeDataCard.py --inputDir /raid/raid7/lucien/Higgs/DarkZ/StatInput/DarkPhotonSelection_m4l118To130_Nominal/2018-10-25_DarkPhotonSR-Unblinding/ --outputDir DataCard/2018-10-25_35p9_Unblinding/
#python makeDataCard.py --inputDir /raid/raid7/lucien/Higgs/DarkZ/StatInput/DarkPhotonSelection_m4l118To130_Nominal/2018-11-09_DarkPhotonSR-150fb-Unblinding/ --outputDir DataCard/2018-11-09_150p0_Unblinding/

#python makeDataCardV2.py --inputDir /raid/raid7/lucien/Higgs/DarkZ/ParaInput/DarkPhotonSelection_m4l118To130_Nominal/2018-11-15_DarkPhotonSR-Unblinding/ --outputDir DataCard/2018-11-15_150p0_Unblinding_NoSB/ --verbose
#python makeDataCardV2.py --inputDir /raid/raid7/lucien/Higgs/DarkZ/ParaInput/DarkPhotonSelection_m4l118To130_Nominal/2018-11-15_DarkPhotonSR-Unblinding/ --outputDir DataCard/2018-11-15_150p0_Unblinding/ --verbose --sideband

#python makeParaCard.py --inputDir /raid/raid7/lucien/Higgs/DarkZ/ParaInput/DarkPhotonSelection_m4l118To130_Nominal/2018-11-21_DarkPhotonSR-Unblinding_Norm/ --verbose --outputDir DataCard/2018-11-22_150p0_ParametricShape/
#python makeParaCard.py --inputDir /raid/raid7/lucien/Higgs/DarkZ/ParaInput/DarkPhotonSelection_m4l118To130_Nominal/2018-11-21_DarkPhotonSR_mZ2-35_Norm/ --verbose --outputDir DataCard/2018-11-22_150p0_ParametricShape_v2/
#python makeParaCard.py --inputDir /raid/raid7/lucien/Higgs/DarkZ/ParaInput/DarkPhotonSelection_m4l118To130_Nominal/2018-11-21_DarkPhotonSR_mZ2-35_Norm/ --verbose --outputDir DataCard/2018-11-26_150p0_ParametricShape_v2/ --parametric --drawDir /home/lucien/public_html/Higgs/DarkZ/StatFW/2018-11-26_Parametrization/
#python makeParaCard.py --inputDir /raid/raid7/lucien/Higgs/DarkZ/ParaInput/DarkPhotonSelection_m4l118To130_Nominal/2018-11-21_DarkPhotonSR_mZ2-35_Norm/ --verbose --outputDir DataCard/2018-11-26_150p0_ParametricShape_rebin_v3/
#python makeParaCard.py --inputDir /raid/raid7/lucien/Higgs/DarkZ/ParaInput/DarkPhotonSelection_m4l118To130_Nominal/2018-11-21_DarkPhotonSR_mZ2-35_Norm/ --verbose --outputDir DataCard/2018-11-26_150p0_ParametricShape_rebin_v4/ --parametric

#python makeParaCard.py --inputDir /raid/raid7/lucien/Higgs/DarkZ/ParaInput/DarkPhotonSelection_m4l118To130_Nominal/2018-11-21_DarkPhotonSR_mZ2-35_Norm/ --verbose --outputDir DataCard/2018-11-26_150p0_ParametricShape_rebin_v5/ --parametric --drawDir ~/public_html/Higgs/DarkZ/StatFW/2018-11-26_150p0_ParametricShape_rebin_v5/

#python makeParaCard.py --inputDir /raid/raid7/lucien/Higgs/DarkZ/ParaInput/DarkPhotonSelection_m4l118To130_Nominal/2018-11-21_DarkPhotonSR_mZ2-35_Norm/ --verbose --outputDir DataCard/2018-11-26_150p0_ParametricShape_rebin_v6/ --parametric

#python makeDataCardV2.py --inputDir /raid/raid7/lucien/Higgs/DarkZ/ParaInput/DarkPhotonSelection_m4l118To130_Nominal/2018-11-21_DarkPhotonSR_mZ2-35_Norm/ --outputDir DataCard/2018-11-27_150p0_Unblinding_NoSB/ --verbose

#python makeParaCard.py --inputDir /raid/raid7/lucien/Higgs/DarkZ/ParaInput/DarkPhotonSelection_m4l118To130_Nominal/2018-11-21_DarkPhotonSR_mZ2-35_Norm/ --verbose --outputDir DataCard/2018-11-28_150p0_ParametricShape_rebin_v7/ --parametric --drawDir ~/public_html/Higgs/DarkZ/StatFW/2018-11-28_150p0_ParametricShape_rebin_v7/
#python makeParaCard.py --inputDir /raid/raid7/lucien/Higgs/DarkZ/ParaInput/DarkPhotonSelection_m4l118To130_Nominal/2018-11-21_DarkPhotonSR_mZ2-35_Norm/ --verbose --outputDir DataCard/2018-11-28_150p0_ParametricShape_rebin_v10/ --parametric --drawDir ~/public_html/Higgs/DarkZ/StatFW/2018-11-28_150p0_ParametricShape_rebin_v10/
#python makeParaCard.py --inputDir /raid/raid7/lucien/Higgs/DarkZ/ParaInput/DarkPhotonSelection_m4l118To130_Nominal/2018-11-21_DarkPhotonSR_mZ2-35_Norm/ --verbose --outputDir DataCard/2018-11-28_150p0_ParametricShape_SignalBW/ --parametric --drawDir ~/public_html/Higgs/DarkZ/StatFW/2018-11-28_150p0_ParametricShape_SignalBW/
python makeParaCard.py --inputDir /raid/raid7/lucien/Higgs/DarkZ/ParaInput/DarkPhotonSelection_m4l118To130_Nominal/2018-11-21_DarkPhotonSR_mZ2-35_Norm/ --verbose --outputDir DataCard/2018-11-29_150p0_ParametricShape_SignalDCB/ --parametric --drawDir ~/public_html/Higgs/DarkZ/StatFW/2018-11-29_150p0_ParametricShape_SignalDCB/

#python makeDataCardV2.py --inputDir /raid/raid7/lucien/Higgs/DarkZ/ParaInput/DarkPhotonSelection_m4l118To130_Nominal/2018-11-21_DarkPhotonSR_mZ2-35_Norm/ --outputDir DataCard/2018-11-28_150p0_Unblinding_NoSB/ --verbose
