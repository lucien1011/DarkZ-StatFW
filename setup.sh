export PYTHONPATH=${PYTHONPATH}:${PWD}/
export PATH=${PATH}:${PWD}/bin/

export BASE_PATH=${PWD}

if [[ $HOSTNAME == *"lxplus"* ]] ;
then
    echo "In LXPLUS" ; 
    cd /afs/cern.ch/work/k/klo/HiggsComb/CMSSW_8_1_0/src/ ; 
elif [[ $HOSTNAME == *"ihepa"* ]] ;
then
    echo "In IHEPA" ; 
    cd /home/lucien/Higgs/DarkZ/Combine/CMSSW_8_1_0/src/ ;
elif [[ $HOSTNAME == *"ufhpc"* ]] ;
then
    echo "In UF HPG" ; 
    cd /home/kinho.lo/Higgs/CombineArea/CMSSW_8_1_0/src/ ;
elif [[ $HOSTNAME == *"lucien"* ]] ;
then
    continue
fi
eval `scramv1 runtime -sh`
cd -
