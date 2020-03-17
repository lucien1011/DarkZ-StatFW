#!/bin/bash

for f in $(ls ./) ; do echo ${f} ; gfal-mkdir gsiftp://cmsio.rc.ufl.edu/cms/data/store/user/klo/HiggsCombineWorkspace/HIG-19-007/XX_2020-03-15_SR2D_RunII/${f} ; gfal-copy -r ${f} gsiftp://cmsio.rc.ufl.edu/cms/data/store/user/klo/HiggsCombineWorkspace/HIG-19-007/XX_2020-03-15_SR2D_RunII/${f} ; done
