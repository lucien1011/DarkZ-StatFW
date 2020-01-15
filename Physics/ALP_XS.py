from StatFW.BaseObject import BaseObject

# ____________________________________________________________________________________________________________________________________________ ||
higgs_boson = BaseObject(
        "Higgs Boson",
        xs = 48.58,
        total_width= 6.1E-03,
        mass = 125.18,
        ZZ_br = 2.64E-02,
        llll_br = 0.0002768,
        vev = 246.33,
        )
z_boson = BaseObject(
        "Z boson",
        mass = 90.,
        ll_br = 0.0679,
        )
ALP = BaseObject(
        "ALP",
        ll_br = 0.1,
        )

mass_points             = range(4,35)
#mass_points            = range(4,63)

# ____________________________________________________________________________________________________________________________________________ ||
def lambda_x_y_func(x,y):
    return (1.-x-y)**2-4.*x*y

def Gamma_hToZa_func(c_zh_div_Lambda,m_a):
    return higgs_boson.mass**3*c_zh_div_Lambda**2*lambda_x_y_func((z_boson.mass/higgs_boson.mass)**2,(m_a/higgs_boson.mass)**2)**1.5

