#!/bin/bash

#inFilePattern="/cms/data/store/user/klo/HiggsCombine/ZZd_HybridNew_2019-12-17_CutAndCount_m4lSR-HZZd_RunII/*/*/*/*/*/*.tar"
#outTarDir=/cms/data/store/user/t2/users/klo/HiggsCombine/ZZd_HybridNew_2019-12-17_CutAndCount_m4lSR-HZZd_RunII/
inFilePattern="/cms/data/store/user/klo/HiggsCombine/ZdZd_HybridNew_2019-12-17_SR2D_RunII/*/*/*/*/*/combine_output_1.tar"
outTarDir=/cms/data/store/user/t2/users/klo/HiggsCombine/ZdZd_HybridNew_2019-12-17_SR2D_RunII/
selectStr=Zd_MZD
poiStr=r,BrHXX_Br2Xll
plotPath=plots/ZdZd/ObsLimit.pdf

python untar_crab.py --pattern=${inFilePattern} --outputDir=${outTarDir} 
python PlotScript/plotHybridNewLimit.py --inputDir ${outTarDir} --selectStr ${selectStr} --poi ${poiStr} --outputPath ${plotPath}
