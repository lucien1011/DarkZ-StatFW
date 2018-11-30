#!/bin/bash

declare -a arr_dir=(
"DataCard/2018-11-30_150p0_ParametricShape_SignalDCB_HiggsRateParam/" 
"DataCard/2018-11-30_150p0_ParametricShape_SignalDCB/" 
"DataCard/2018-11-30_150p0_Unblinding_NoSB/"
"DataCard/2018-11-30_150p0_Unblinding/"
)

for m in 7 10 15 20 25 30 ; 
do 
    echo "-----------------------------------" ; 
    echo "MZd ${m}" ; 
    for i in "${arr_dir[@]}" ;
    do
        #echo "===================================" ;
        echo ${i}; 
        cat ${i}HZZd_M${m}/AsymptoticLimits_Out.txt | grep "Expected 50.0%" ; 
    done
done
