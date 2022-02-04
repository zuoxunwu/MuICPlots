# MuICStudies

Simple scripts to make plots for MuIC studies.
To setup

`git clone git@github.com:zuoxunwu/MuICPlots.git MuICPlots`

Does not rely much on running environment, just need python and ROOT. On lxplus, it can be setup by

`source /cvmfs/sft.cern.ch/lcg/views/LCG_99/x86_64-centos7-gcc10-opt/setup.sh`

To run the script, for example, just do 

`python3 scripts/plot_vs_eMu.py`


### Remark

Some scripts, like `scripts/kinematic_dist.py`, has some hard-coded library path and input files. 
It does not work as-is. Remember to change it to your need before using it.
