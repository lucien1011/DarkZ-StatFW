import os,copy,math,argparse,glob
from Utilities.mkdir_p import mkdir_p

#orig_dir            = "/cms/data/store/user/t2/users/klo/HiggsCombine/2020-03-17_SR2D_RunII_El_LHCLimit_v2_ext1/"
#ext_dir             = "/cms/data/store/user/t2/users/klo/HiggsCombine/2020-03-17_SR2D_RunII_El_LHCLimit_v2/"
#out_dir             = "/cms/data/store/user/t2/users/klo/HiggsCombine/2020-03-17_SR2D_RunII_El_LHCLimit_v2/"

#orig_dir            = "/cms/data/store/user/t2/users/klo/HiggsCombine/2020-03-17_SR2D_RunII_Mu_LHCLimit_v2_ext1/"
orig_dir            = "/cms/data/store/user/t2/users/klo/HiggsCombine/2020-03-17_SR2D_RunII_Mu_LHCLimit_v2_ext2/"
ext_dir             = "/cms/data/store/user/t2/users/klo/HiggsCombine/2020-03-17_SR2D_RunII_Mu_LHCLimit_v2/"
out_dir             = "/cms/data/store/user/t2/users/klo/HiggsCombine/2020-03-17_SR2D_RunII_Mu_LHCLimit_v2/"

#orig_dir            = "/cms/data/store/user/t2/users/klo/HiggsCombine/2020-03-17_SR2D_RunII_LHCLimit_v2_ext2/"
#ext_dir             = "/cms/data/store/user/t2/users/klo/HiggsCombine/2020-03-17_SR2D_RunII_LHCLimit_v2/"
#out_dir             = "/cms/data/store/user/t2/users/klo/HiggsCombine/2020-03-17_SR2D_RunII_LHCLimit_v2/"

#orig_dir            = "/cms/data/store/user/t2/users/klo/HiggsCombine/2020-03-17_SR2D_RunII_LHCLimit_v2_ext3/"
#ext_dir             = "/cms/data/store/user/t2/users/klo/HiggsCombine/2020-03-17_SR2D_RunII_LHCLimit_v2/"
#out_dir             = "/cms/data/store/user/t2/users/klo/HiggsCombine/2020-03-17_SR2D_RunII_LHCLimit_v2/"

orig_file_name      = "gridd.root"
ext_file_name       = "gridd_hadd.root"
out_file_name       = "gridd_hadd2.root"

select_str  = "Zd_MZD*"

for path in glob.glob(os.path.join(orig_dir,select_str)):
    dir_name = path.split("/")[-1]
    hadd_cmd = " ".join(["hadd","-f",os.path.join(out_dir,dir_name,out_file_name),os.path.join(orig_dir,dir_name,orig_file_name),os.path.join(ext_dir,dir_name,ext_file_name)])
    os.system(hadd_cmd)
