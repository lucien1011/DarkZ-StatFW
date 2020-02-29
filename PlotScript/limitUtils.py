from Physics.Zd_XS import *
from Physics.ALP_XS import *
import math

y_label_dict    = {
                    "r": "Signal strength",
                    "epsilon": "#varepsilon",
                    "epsilon_EpsPOI": "#varepsilon",
                    "kappa": "#kappa",
                    "BrHZZd": "Br(h #rightarrow Z Z_{d})",
                    "BrHZZd_Interpolation": "Br(h #rightarrow Z Z_{d})",
                    "BrHZdZd": "Br(h #rightarrow Z_{d} Z_{d})",
                    "BrHZdZd_Interpolation": "Br(h #rightarrow Z_{d} Z_{d})",
                    "BrH4l": "Br(h #rightarrow ZX #rightarrow 4#mu)",
                    "c_zh_div_Lambda_Interpolation": "|C^{eff}_{Zh}|/#Lambda [TeV^{-1}]",
                    "c_ah_div_Lambda_Interpolation": "|C^{eff}_{ah}|/#Lambda^{2} [TeV^{-2}]",
                    "xs_ZZd": "Cross section [pb]",
                    "xs_ZdZd": "Cross section [pb]",
                    "BrHZX_BrXll": "Br(h #rightarrow Z X) #times Br(X #rightarrow ll)",
                    "BrHZX_BrXMuMu": "Br(h #rightarrow Z X) #times Br(X #rightarrow #mu #mu)",
                    "BrHZX_BrXee": "Br(h #rightarrow Z X) #times Br(X #rightarrow ee)",
                    "BrHXX_Br2Xll": "Br(h #rightarrow X X) #times Br(X #rightarrow ll)^{2}",
                    "BrHXX_Br2XMuMu": "Br(h #rightarrow X X) #times Br(X #rightarrow #mu #mu)^{2}",
                    "BrHXX_Br2Xee": "Br(h #rightarrow X X) #times Br(X #rightarrow ee)^{2}",
                    #"BrH4l": "Br(h #rightarrow ZX #rightarrow 4e)",
                  }

def calculate(r_value,window_value,what):
    if what == "epsilon":
        return epsilon*math.sqrt(r_value)
    elif what == "kappa":
        return kappa*math.sqrt(r_value)
    elif what == "BrHZdZd":
        return r_value*xs_HZdZd_dict[window_value]/xs_brHZdZd_dict[window_value]
    elif what == "BrHZZd":
        return r_value*xs_dict[window_value]/xs_brHZZd_dict[window_value]
    elif what == "BrHZZd_Interpolation":
        return r_value*(higgs_xs*epsilon**2*reader.interpolate(window_value,"Br_HToZZdTo4l"))/(higgs_xs*reader.interpolate(window_value,"Br_ZdTo2l")*z_2l_br)
    elif what == "BrHZdZd_Interpolation":
        return r_value*(higgs_xs*kappa**2*reader.interpolate(window_value,"Br_HToZdZdTo4l"))/(higgs_xs*reader.interpolate(window_value,"Br_ZdTo2l")**2)
    elif what == "BrHZX_BrXll":
        return r_value*(epsilon**2*reader.interpolate(window_value,"Br_HToZZdTo4l"))/z_2l_br
    elif what == "BrHZX_BrXMuMu":
        return r_value*(epsilon**2*reader.interpolate(window_value,"Br_HToZZdTo4l"))/(z_2l_br/2.)
    elif what == "BrHZX_BrXee":
        return r_value*(epsilon**2*reader.interpolate(window_value,"Br_HToZZdTo4l"))/(z_2l_br/2.)
    elif what == "BrHXX_Br2Xll":
        return r_value*(kappa**2*reader.interpolate(window_value,"Br_HToZdZdTo4l"))
    elif what == "BrHXX_Br2XMuMu":
        return r_value*(kappa**2*reader.interpolate(window_value,"Br_HToZdZdTo4l"))
    elif what == "BrHXX_Br2Xee":
        return r_value*(kappa**2*reader.interpolate(window_value,"Br_HToZdZdTo4l"))
    elif what == "epsilon_EpsPOI":
        return r_value
    elif what == "BrH4l":
        return r_value*xs_dict[window_value]/higgs_xs
    elif what == "r":
        return r_value
    elif what == "xs_ZZd":
        return r_value*(higgs_boson.xs*epsilon**2*reader.interpolate(window_value,"Br_HToZZdTo4l"))
    elif what == "xs_ZdZd":
        return r_value*(higgs_boson.xs*kappa**2*reader.interpolate(window_value,"Br_HToZdZdTo4l"))
    elif what == "c_zh_div_Lambda_Interpolation":
        ratio_exc = r_value*(higgs_boson.xs*epsilon**2*reader.interpolate(window_value,"Br_HToZZdTo4l"))/higgs_boson.xs/z_boson.ll_br/reader.interpolate(window_value,"Br_ZdTo2l")
        Gamma_hToZa_exc = ratio_exc*higgs_boson.total_width/(1.-ratio_exc)
        return math.sqrt(Gamma_hToZa_exc*16.*math.pi/higgs_boson.mass**3/lambda_x_y_func((z_boson.mass/higgs_boson.mass)**2,(window_value/higgs_boson.mass)**2)**1.5)*1000
    elif what == "c_ah_div_Lambda_Interpolation":
        ratio_exc = r_value*(higgs_boson.xs*kappa**2*reader.interpolate(window_value,"Br_HToZdZdTo4l"))/higgs_boson.xs/reader.interpolate(window_value,"Br_ZdTo2l")**2
        Gamma_hToaa_exc = ratio_exc*higgs_boson.total_width/(1.-ratio_exc)
        return math.sqrt(Gamma_hToaa_exc*32.*math.pi/higgs_boson.mass**3/higgs_boson.vev**2/(1.-2.*window_value**2/higgs_boson.mass**2)**2/math.sqrt(1.-4.*window_value**2/higgs_boson.mass**2))*1000*1000
    else:
        raise RuntimeError


