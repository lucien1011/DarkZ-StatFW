#!/bin/bash

for m in 4 7 10 15 20 25 30 ; 
do 
    #python makeWorkspace.py --inputDir DataCard/2018-10-23_Unblinding/window_${m}_0p02/
    #python makeWorkspace.py --inputDir DataCard/2018-10-24_Unblinding/window_${m}_0p02/
    #python makeWorkspace.py --inputDir DataCard/2018-10-25_Unblinding/window_${m}_0p02/
    #python makeWorkspace.py --inputDir DataCard/2018-10-25_35p9_Unblinding/window_${m}_0p02/
    #python makeWorkspace.py --inputDir DataCard/2018-11-09_150p0_Unblinding/window_${m}_0p02/
    python makeWorkspace.py --inputDir DataCard/2018-11-15_150p0_Unblinding/HZZd_M${m}/ --pattern "HZZd_*.txt"
    python makeWorkspace.py --inputDir DataCard/2018-11-15_150p0_Unblinding_NoSB/HZZd_M${m}/ --pattern "HZZd_*.txt"
done
