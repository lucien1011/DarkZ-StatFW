from StatFW.BaseObject import BaseObject
import math

# ____________________________________________________________________________________________________________________________________________ ||
higgs_boson = BaseObject(
        "Higgs Boson",
        xs = 48.58,
        total_width= 4.1E-03,
        mass = 125.18,
        ZZ_br = 2.64E-02,
        llll_br = 0.0002768,
        vev = 246.33,
        )
z_boson = BaseObject(
        "Z boson",
        mass = 91.1876,
        #ll_br = 0.0679,
        ll_br = 0.06729,
        )
ALP = BaseObject(
        "ALP",
        ll_br = 1.0,
        )

mass_points             = range(4,35)
#mass_points            = range(4,63)

# ____________________________________________________________________________________________________________________________________________ ||
def lambda_x_y_func(x,y):
    return (1.-x-y)**2-4.*x*y

def Gamma_hToZa_func(c_zh_div_Lambda,m_a):
    return (higgs_boson.mass**3)*(c_zh_div_Lambda**2)*(lambda_x_y_func((z_boson.mass/higgs_boson.mass)**2,(m_a/higgs_boson.mass)**2)**1.5)/16./math.pi

def Gamma_HToaa_func(c_ah_div_Lambda,m_a):
    return higgs_boson.vev**2*(higgs_boson.mass**3)*c_ah_div_Lambda**2*(1.-2.*(m_a**2)/higgs_boson.mass**2)**2*math.sqrt(1.-4.*(m_a**2)/higgs_boson.mass**2)/32./math.pi

def zh_acc_ratio(mass):
    return 0.22/31.*mass + 1.-0.22/31.*35.

def ah_acc_ratio(mass):
    return 0.22/56.*mass + 1.-0.22/56.*60.
