#!/bin/bash

#inputDir=HToZdZd_DataCard/2020-03-17_SR2D_RunII/
#targetDir=/cms/data/store/user/klo/HiggsCombineWorkspace/HIG-19-007/XX_2020-03-17_SR2D_RunII/

#inputDir=HToZdZd_DataCard/2020-03-17_SR2D_RunII_Mu/
#targetDir=/cms/data/store/user/klo/HiggsCombineWorkspace/HIG-19-007/XX_2020-03-17_SR2D_RunII_Mu/

#inputDir=HToZdZd_DataCard/2020-03-17_SR2D_RunII_El/
#targetDir=/cms/data/store/user/klo/HiggsCombineWorkspace/HIG-19-007/XX_2020-03-17_SR2D_RunII_El/

#inputDir=DataCard/2020-03-03_CutAndCount_m4lSR-HZZd_RunII/
#targetDir=/cms/data/store/user/klo/HiggsCombineWorkspace/HIG-19-007/ZX_2020-03-03_CutAndCount_m4lSR-HZZd_RunII/

#inputDir=DataCard/2020-03-03_CutAndCount_m4lSR-HZZd_RunII_Mu/
#targetDir=/cms/data/store/user/klo/HiggsCombineWorkspace/HIG-19-007/ZX_2020-03-03_CutAndCount_m4lSR-HZZd_RunII_Mu/

inputDir=DataCard/2020-03-03_CutAndCount_m4lSR-HZZd_RunII_El/
targetDir=/cms/data/store/user/klo/HiggsCombineWorkspace/HIG-19-007/ZX_2020-03-03_CutAndCount_m4lSR-HZZd_RunII_El/

for f in $(ls ${inputDir}) ; 
do 
    echo ${f} ; 
    gfal-mkdir gsiftp://cmsio.rc.ufl.edu/${targetDir}${f} ; 
    gfal-copy -r ${inputDir}${f} gsiftp://cmsio.rc.ufl.edu/${targetDir}${f} ; 
done
