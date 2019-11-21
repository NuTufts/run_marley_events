#!/bin/bash

#SBATCH --job-name=cenns750
#SBATCH --output=cenns750_0.log
#SBATCH --mem-per-cpu=4000
#SBATCH --time=1-00:00:00
#SBATCH --array=0

CONTAINER=/cluster/tufts/wongjiradlab/twongj01/coherent/singularity-geant4-10.02.p03.simg

WORKDIR=/cluster/tufts/wongjiradlab/twongj01/coherent/run_marley_events

FILELIST=$WORKDIR/filelist.txt
TEMPLATE=$WORKDIR/template.mac
CENNSDIR=/cluster/tufts/wongjiradlab/twongj01/coherent/cenns10geant4
OUTDIR=$WORKDIR/outdir

module load singularity
singularity exec $CONTAINER bash -c "cd $WORKDIR && source run_marley_job.sh $FILELIST $TEMPLATE $CENNSDIR $WORKDIR $OUTDIR"
