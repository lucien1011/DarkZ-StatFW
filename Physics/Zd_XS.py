epsilon     = 0.05
higgs_xs    = 48.58
sm_br_4l_xs = higgs_xs*0.0002768
z_2l_br     = 0.06729
h_ZZ_br     = 2.64E-02
kappa       = 0.001

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

xs_HZdZd_dict = {
        4:      higgs_xs*kappa**2*139.6979988681,
        5:      higgs_xs*kappa**2*116.344056810798,
        6:      higgs_xs*kappa**2*114.597532012221,
        7:      higgs_xs*kappa**2*104.179322296929,
        8:      higgs_xs*kappa**2*104.468186168107,
        9:      higgs_xs*kappa**2*103.60243300267,
        10:     higgs_xs*kappa**2*102.438053362877,
        15:     higgs_xs*kappa**2*90.2249218877198,
        20:     higgs_xs*kappa**2*83.4164181430647,
        25:     higgs_xs*kappa**2*75.0753462796701,
        30:     higgs_xs*kappa**2*65.8037628468827,
        35:     higgs_xs*kappa**2*56.0744652388090,
        40:     higgs_xs*kappa**2*46.378435893888,
        45:     higgs_xs*kappa**2*37.0703510401361,
        50:     higgs_xs*kappa**2*28.2300329469609,
        55:     higgs_xs*kappa**2*19.6174575765711,
        60:     higgs_xs*kappa**2*10.079694787684147,
        }

xs_brHZdZd_dict = {
        4:      higgs_xs*0.344**2,
        5:      higgs_xs*0.315**2,
        6:      higgs_xs*0.313**2,
        7:      higgs_xs*0.299**2,
        8:      higgs_xs*0.301**2,
        9:      higgs_xs*0.300**2,
        10:     higgs_xs*0.300**2,
        15:     higgs_xs*0.288**2,
        20:     higgs_xs*0.286**2,
        25:     higgs_xs*0.283**2,
        30:     higgs_xs*0.280**2,
        35:     higgs_xs*0.274**2,
        40:     higgs_xs*0.267**2,
        45:     higgs_xs*0.251**2,
        50:     higgs_xs*0.244**2,
        55:     higgs_xs*0.227**2,
        60:     higgs_xs*0.206**2,
        }
