#!/bin/bash

#python runCombineTask.py --inputDir DataCard/2018-10-23_Unblinding/ --selectStr "window"
#python runCombineTask.py --inputDir DataCard/2018-10-24_Unblinding/ --selectStr "window"
#python runCombineTask.py --inputDir DataCard/2018-10-25_Unblinding/ --selectStr "window"
#python runCombineTask.py --inputDir DataCard/2018-10-25_35p9_Unblinding/ --selectStr "window"
#python runCombineTask.py --inputDir DataCard/2018-10-24_Unblinding_NoSyst/ --selectStr "window" --option='--systematics=0'
#python runCombineTask.py --inputDir DataCard/2018-11-09_150p0_Unblinding/ --selectStr "window"
python runCombineTask.py --inputDir DataCard/2018-11-15_150p0_Unblinding_NoSB/ --selectStr "HZZd" --pattern "HZZd_M*.root"
python runCombineTask.py --inputDir DataCard/2018-11-15_150p0_Unblinding/ --selectStr "HZZd" --pattern "HZZd_M*.root"
