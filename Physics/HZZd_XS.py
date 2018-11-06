epsilon     = 0.05
higgs_xs    = 48.58
sm_br_4l_xs = higgs_xs*0.0002768
z_2l_br     = 0.06729
h_ZZ_br     = 2.64E-02

xs_dict = {
        4:      higgs_xs*epsilon**2*0.000219,
        7:      higgs_xs*epsilon**2*0.000597,
        10:     higgs_xs*epsilon**2*0.00126,
        15:     higgs_xs*epsilon**2*(0.00252+0.00338)/2.,
        20:     higgs_xs*epsilon**2*0.00555,
        25:     higgs_xs*epsilon**2*(0.00814+0.00940)/2.,
        30:     higgs_xs*epsilon**2*0.0108,
        }

xs_brHZZd_dict = {
        4:      higgs_xs*0.344*z_2l_br,
        7:      higgs_xs*0.299*z_2l_br,
        10:     higgs_xs*0.300*z_2l_br,
        15:     higgs_xs*0.288*z_2l_br,
        20:     higgs_xs*0.286*z_2l_br,
        25:     higgs_xs*0.283*z_2l_br,
        30:     higgs_xs*0.280*z_2l_br,
        }
