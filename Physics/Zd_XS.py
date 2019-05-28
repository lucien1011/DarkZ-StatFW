from BrTableReader import *
import os

# ____________________________________________________________________________________________________________________________________________ ||
zdTextFile = open(os.environ["BASE_PATH"]+"/Physics/HiggsedDarkPhoton_BrTableData.txt","r")
lines = zdTextFile.readlines()
reader = BrTableReader()

for l in lines: # skip the first line as it is header
    if l.startswith("#"): continue
    mass,Gamma_Zd,Br_ZdTo2l,Br_HToZZdTo4l,Br_HToZdZdTo4l = map(float,l.split())
    reader.addInfo(mass,Gamma_Zd,Br_ZdTo2l,Br_HToZZdTo4l,Br_HToZdZdTo4l)

# ____________________________________________________________________________________________________________________________________________ ||
epsilon     = 0.05
higgs_xs    = 48.58
sm_br_4l_xs = higgs_xs*0.0002768
z_2l_br     = 0.06729
h_ZZ_br     = 2.64E-02
kappa       = 0.001
#mass_points = range(4,35)
mass_points = range(4,61)

# ____________________________________________________________________________________________________________________________________________ ||
xs_dict = {}
xs_brHZZd_dict = {}
xs_HZdZd_dict = {}
xs_brHZdZd_dict = {}
for m in mass_points:
    if m <= 12 or m % 2 == 0:
        xs_dict[m] = higgs_xs*epsilon**2*reader.infoDict[m].Br_HToZZdTo4l
        xs_brHZZd_dict[m] = higgs_xs*reader.infoDict[m].Br_ZdTo2l*z_2l_br
        xs_HZdZd_dict[m] = higgs_xs*kappa**2*reader.infoDict[m].Br_HToZdZdTo4l
        xs_brHZdZd_dict[m] = higgs_xs*reader.infoDict[m].Br_ZdTo2l**2
    else:
        xs_dict[m] = higgs_xs*epsilon**2*(reader.infoDict[m-1].Br_HToZZdTo4l+reader.infoDict[m+1].Br_HToZZdTo4l)/2.
        xs_brHZZd_dict[m] = higgs_xs*(reader.infoDict[m-1].Br_ZdTo2l+reader.infoDict[m+1].Br_ZdTo2l)/2.*z_2l_br
        xs_HZdZd_dict[m] = higgs_xs*kappa**2*(reader.infoDict[m-1].Br_HToZdZdTo4l+reader.infoDict[m+1].Br_HToZdZdTo4l)/2.
        xs_brHZdZd_dict[m] = higgs_xs*((reader.infoDict[m-1].Br_ZdTo2l+reader.infoDict[m+1].Br_ZdTo2l)/2.)**2
