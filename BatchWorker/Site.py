import os

class Site(object):
    cern_str = "CERN"
    ihepa_str = "IHEPA"
    def where_am_i(self):
        if "lxplus" in os.environ["HOSTNAME"]: return "CERN"
        elif "ihepa" in os.environ["HOSTNAME"]: return "IHEPA"
