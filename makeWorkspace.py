import glob,os

inputDir = "/home/lucien/Higgs/DarkZ/DarkZ-StatFW/DataCard/2018-08-17/"
pattern = "window_*.txt"

for textFileName in glob.glob(inputDir+pattern):
    print "*"*20
    print "Making workspace from", textFileName
    cmd = "text2workspace.py "+textFileName
    os.system(cmd)

