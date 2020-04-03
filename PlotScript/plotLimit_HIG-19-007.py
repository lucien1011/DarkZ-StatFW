from Physics.ALP_XS import *
from Physics.Zd_XS import * 
from PlotScript.limitUtils import y_label_dict,calculate

import ROOT,glob,os,subprocess,array,math
from collections import OrderedDict
import CMS_lumi 
import tdrstyle 

from StatFW.BaseObject import BaseObject

ROOT.gROOT.SetBatch(ROOT.kTRUE)

# ________________________________________________________________ ||
# CMS style
# ________________________________________________________________ ||
CMS_lumi.cmsText = "CMS"
CMS_lumi.extraText = ""
ROOT.TGaxis.SetMaxDigits(8)
CMS_lumi.cmsTextSize = 0.65
CMS_lumi.outOfFrame = True
CMS_lumi.lumi_13TeV = "136.1 fb^{-1}"
tdrstyle.setTDRStyle()
