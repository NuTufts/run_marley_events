#!/bin/bash

energy=$1
template=$2
cennsdir=$3
workdir=$4
outdir=$5


# setup container
source /usr/local/root/root-6.16.00/bin/thisroot.sh 
source /usr/local/geant/geant4.10.02.p03/bin/geant4.sh 

# setup CENNS
cd $cennsdir
source setenv.sh

# go to workdir
cd $workdir

# get inputfile from file list
let ienergy=${SLURM_ARRAY_TASK_ID}

inputfile=`printf $workdir/cc_configs/cc_marley_mono_Ev%02d.json ${ienergy}`
echo "input marley config file: $inputfile"

# jobdir
jobdir=`printf ${workdir}/slurm_cc_job%03d ${SLURM_ARRAY_TASK_ID}`
mkdir -p $jobdir
cd $jobdir

# output file
outfile=`printf cc_marleyout_Ev%02d_00_gen.root $energy`
echo "output file: ${outfile}"

# make macro
cp $template macro.mac
sed -i 's|MARLEYCONFIGFILE|'"${inputfile}"'|g' macro.mac
sed -i 's/JSONOUTFILE/'"${outfile}"'/g'  macro.mac

#CENNS -m macro.mac > /dev/null
CENNS -m macro.mac # for debug

mv $outfile $outdir/