#!/bin/bash

#for m in 4 7 10 15 20 25 30 ; 
for m in 4 5 6 7 8 9 10 15 20 25 30 35 40 45 50 55 60; 
do 
    #python makeWorkspace.py --inputDir DataCard/2018-10-23_Unblinding/window_${m}_0p02/
    #python makeWorkspace.py --inputDir DataCard/2018-10-24_Unblinding/window_${m}_0p02/
    #python makeWorkspace.py --inputDir DataCard/2018-10-25_Unblinding/window_${m}_0p02/
    #python makeWorkspace.py --inputDir DataCard/2018-10-25_35p9_Unblinding/window_${m}_0p02/
    #python makeWorkspace.py --inputDir DataCard/2018-11-09_150p0_Unblinding/window_${m}_0p02/
    #python makeWorkspace.py --inputDir DataCard/2018-11-15_150p0_Unblinding/HZZd_M${m}/ --pattern "HZZd_*.txt"
    #python makeWorkspace.py --inputDir DataCard/2018-11-15_150p0_Unblinding_NoSB/HZZd_M${m}/ --pattern "HZZd_*.txt"
    #python makeWorkspace.py --inputDir DataCard/2018-11-22_150p0_ParametricShape/HZZd_M${m}/ --pattern "HZZd_*.txt"
    #python makeWorkspace.py --inputDir DataCard/2018-11-22_150p0_ParametricShape_v2/HZZd_M${m}/ --pattern "HZZd_*.txt"
    #python makeWorkspace.py --inputDir DataCard/2018-11-26_150p0_ParametricShape_v2/HZZd_M${m}/ --pattern "HZZd_*.txt"
    #python makeWorkspace.py --inputDir DataCard/2018-11-26_150p0_ParametricShape_rebin_v2/HZZd_M${m}/ --pattern "HZZd_*.txt"
    #python makeWorkspace.py --inputDir DataCard/2018-11-26_150p0_ParametricShape_rebin_v4/HZZd_M${m}/ --pattern "HZZd_*.txt"
    #python makeWorkspace.py --inputDir DataCard/2018-11-26_150p0_ParametricShape_rebin_v5/HZZd_M${m}/ --pattern "HZZd_*.txt"
    #python makeWorkspace.py --inputDir DataCard/2018-11-27_150p0_Unblinding_NoSB/HZZd_M${m}/ --pattern "HZZd_*.txt"
    #python makeWorkspace.py --inputDir DataCard/2018-11-27_150p0_Unblinding_NoSB_ParametricNumber/HZZd_M${m}/ --pattern "HZZd_*.txt"
    #python makeWorkspace.py --inputDir DataCard/2018-11-28_150p0_ParametricShape_rebin_v7/HZZd_M${m}/ --pattern "HZZd_*.txt"
    #python makeWorkspace.py --inputDir DataCard/2018-11-28_150p0_ParametricShape_rebin_v10/HZZd_M${m}/ --pattern "HZZd_*.txt"
    #python makeWorkspace.py --inputDir DataCard/2018-11-28_150p0_ParametricShape_SignalBW/HZZd_M${m}/ --pattern "HZZd_*.txt"
    #python makeWorkspace.py --inputDir DataCard/2018-11-29_150p0_ParametricShape_SignalDCB/HZZd_M${m}/ --pattern "HZZd_*.txt"
    #python makeWorkspace.py --inputDir DataCard/2018-11-28_150p0_Unblinding_NoSB/HZZd_M${m}/ --pattern "HZZd_*.txt"

    #python makeWorkspace.py --inputDir DataCard/2018-11-30_150p0_ParametricShape_SignalDCB_HiggsRateParam/HZZd_M${m}/ --pattern "HZZd_*.txt"
    #python makeWorkspace.py --inputDir DataCard/2018-11-30_150p0_Unblinding/HZZd_M${m}/ --pattern "HZZd_*.txt"
    #python makeWorkspace.py --inputDir DataCard/2018-11-30_150p0_Unblinding_NoSB/HZZd_M${m}/ --pattern "HZZd_*.txt"
    #python makeWorkspace.py --inputDir DataCard/2018-11-30_150p0_ParametricShape_SignalDCB/HZZd_M${m}/ --pattern "HZZd_*.txt"
    #python makeWorkspace.py --inputDir DataCard/2018-11-30_150p0_ParametricShape_SignalDCB_HiggsRateParam/HZZd_M${m}/ --pattern "HZZd_*.txt"
    #python makeWorkspace.py --inputDir HToZdZd_DataCard/2019-02-13_test_RatioCut0p05/HToZdZd_MZD${m}/ --pattern "HToZdZd_*.txt"
    #python makeWorkspace.py --inputDir HToZdZd_DataCard/2019-02-15_35p9_RatioCut0p05_MCStatUnc_Width0p05/HToZdZd_MZD${m}/ --pattern "HToZdZd_*.txt"
    #python makeWorkspace.py --inputDir HToZdZd_DataCard/2019-02-18_35p9_RatioCut0p05_MCStatUnc_Width0p05/HToZdZd_MZD${m}/ --pattern "HToZdZd_*.txt"
    #python makeWorkspace.py --inputDir HToZdZd_DataCard/2019-02-18_35p9_RatioCut0p05_MCStatUnc_Width0p01And0p02/HToZdZd_MZD${m}/ --pattern "HToZdZd_*.txt"
    #python makeWorkspace.py --inputDir HToZdZd_DataCard/2019-02-18_35p9_RatioCut0p02And0p01_MCStatUnc/HToZdZd_MZD${m}/ --pattern "HToZdZd_*.txt"
    python makeWorkspace.py --inputDir HToZdZd_DataCard/2019-02-28_35p9_RatioCut0p05_MCStatUnc_Width0p02And0p05/HToZdZd_MZD${m}/ --pattern "HToZdZd_*.txt"
done
