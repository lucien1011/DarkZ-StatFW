import ROOT,math

def getIntegral(hist,overflow=False):
    error = ROOT.Double(0.)
    start_bin = 0 if overflow else 1
    end_bin = hist.GetNbinsX()+1 if overflow else hist.GetNbinsX()
    integral = hist.IntegralAndError(
            start_bin,
            end_bin,
            error,
            )
    return integral,error

def getCountAndError(hist,central,width,isSR=True):
    lower_value = central*(1.-width)
    upper_value = central*(1.+width)

    if isSR:
        error = ROOT.Double(0.)
        integral = hist.IntegralAndError(
                hist.GetXaxis().FindFixBin(lower_value),
                hist.GetXaxis().FindFixBin(upper_value),
                error,
                )
    else:
        error1 = ROOT.Double(0.)
        integral1 = hist.IntegralAndError(
                0,
                hist.GetXaxis().FindFixBin(lower_value)-1,
                error1,
                )
        error2 = ROOT.Double(0.)
        integral2 = hist.IntegralAndError(
                hist.GetXaxis().FindFixBin(upper_value)+1,
                hist.GetNbinsX()+1,
                error2,
                )
        integral = integral1+integral2
        error = math.sqrt(error1**2+error2**2)
    return integral,error

def getBinContentAndError(hist,x1,x2):
    error = ROOT.Double(0.)
    integral = hist.IntegralAndError(
            hist.GetXaxis().FindFixBin(x1),
            hist.GetXaxis().FindFixBin(x2),
            error,
            )
    return integral,error
