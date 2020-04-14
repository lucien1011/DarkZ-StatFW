#!/bin/bash

#inputDir=/cms/data/store/user/t2/users/klo/HiggsCombine/2020-03-17_SR2D_RunII_El_LHCLimit_v2/
inputDir=/cms/data/store/user/t2/users/klo/HiggsCombine/2020-03-17_SR2D_RunII_Mu_LHCLimit_v2/
#inputDir=/cms/data/store/user/t2/users/klo/HiggsCombine/2020-03-17_SR2D_RunII_LHCLimit_v2/
returnDir=${PWD}

cd ${inputDir} 
for d in $(find -name "Zd_MZD*" -type d ) ; 
do
    echo ${d} ;
    cd ${d} ; 
    combine -M HybridNew --LHCmode LHC-limits -T 12000 --readHybridResults --grid gridd_hadd2.root --plot cls_fromgrid_exp025.pdf --expectedFromGrid 0.025 ${d}.root ;
    combine -M HybridNew --LHCmode LHC-limits -T 12000 --readHybridResults --grid gridd_hadd2.root --plot cls_fromgrid_exp16.pdf --expectedFromGrid 0.16 ${d}.root ;
    combine -M HybridNew --LHCmode LHC-limits -T 12000 --readHybridResults --grid gridd_hadd2.root --plot cls_fromgrid_exp50.pdf --expectedFromGrid 0.50 ${d}.root ;
    combine -M HybridNew --LHCmode LHC-limits -T 12000 --readHybridResults --grid gridd_hadd2.root --plot cls_fromgrid_exp840.pdf --expectedFromGrid 0.84 ${d}.root ;
    combine -M HybridNew --LHCmode LHC-limits -T 12000 --readHybridResults --grid gridd_hadd2.root --plot cls_fromgrid_exp975.pdf --expectedFromGrid 0.975 ${d}.root ;
    combine -M HybridNew --LHCmode LHC-limits -T 12000 --readHybridResults --grid gridd_hadd2.root --plot cls_fromgrid.pdf ${d}.root
    cd - ;
done
cd ${returnDir}

