#!/bin/bash

declare -a arr_dir=(
"HToZdZd_DataCard/2019-12-06_SR_RunII/" 
"HToZdZd_DataCard/2019-12-06_SR2D_RunII/"
)

for m in 4 5 6 7 8 9 10 15 20 25 30 35 40 45 50 55 60 ; 
do 
    echo "-----------------------------------" ; 
    echo "MZd ${m}" ; 
    for i in "${arr_dir[@]}" ;
    do
        #echo "===================================" ;
        echo ${i}; 
        cat ${i}Zd_MZD${m}/AsymptoticLimits_Out.txt | grep "Expected 50.0%" ; 
    done
done
