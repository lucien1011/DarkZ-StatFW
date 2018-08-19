import glob,os

inputDir = "/home/lucien/Higgs/DarkZ/DarkZ-StatFW/DataCard/2018-08-17/"
pattern = "window_*.root"
method = "AsymptoticLimits"

for wsFileName in glob.glob(inputDir+pattern):
    print "*"*20
    print "Running on workspace", wsFileName
    cmd = " ".join(["combine","-M",method,wsFileName])
    os.system(cmd)

