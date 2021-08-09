from Physics.ALP_XS import *
import math

c_zh_div_Lambda = 2e-5 
za_masses = [5,10,15,20,25,30]

c_ah_div_Lambda = 1e-8 
aa_masses = [5,15,25,35,45,55]

for m in za_masses:
    g_bsm = Gamma_hToZa_func(c_zh_div_Lambda,m)
    print(m,g_bsm/(g_bsm+higgs_boson.total_width))

for m in aa_masses:
    g_bsm = Gamma_HToaa_func(c_ah_div_Lambda,m)
    print(m,g_bsm/(g_bsm+higgs_boson.total_width))
