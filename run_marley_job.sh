#!/bin/bash

filelist=$1
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
let lineno=${SLURM_ARRAY_TASK_ID}+1
inputfile=`sed -n ${lineno}p $filelist`

echo "inputfile: $inputfile"

# jobdir
jobdir=`printf ${workdir}/slurm_job%03d ${SLURM_ARRAY_TASK_ID}`
mkdir -p $jobdir
cd $jobdir

# output file
outfile=`echo "$(basename ${inputfile})" | sed 's/nc\_out/nc\_marleyout/g' | sed 's/\.json/\.root/g'`
echo "output file: ${outfile}"

# make macro
cp $template macro.mac
sed -i 's|JSONINFILE|'"${inputfile}"'|g' macro.mac
sed -i 's/JSONOUTFILE/'"${outfile}"'/g'  macro.mac

CENNS -m macro.mac > /dev/null

mv $outfile $outdir/