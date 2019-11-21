#!/bin/bash

#SBATCH --job-name=cc_cenns750
#SBATCH --output=cc_cenns750_0.log
#SBATCH --mem-per-cpu=4000
#SBATCH --time=1-00:00:00
#SBATCH --array=30

CONTAINER=/cluster/tufts/wongjiradlab/twongj01/coherent/singularity-geant4-10.02.p03.simg

WORKDIR=/cluster/tufts/wongjiradlab/twongj01/coherent/run_marley_events

ENERGY=30
TEMPLATE=$WORKDIR/cc_template.mac
CENNSDIR=/cluster/tufts/wongjiradlab/twongj01/coherent/cenns10geant4
OUTDIR=$WORKDIR/cc_outdir

module load singularity
mkdir -p $OUTDIR
singularity exec $CONTAINER bash -c "cd $WORKDIR && source run_cc_marley_job.sh $ENERGY $TEMPLATE $CENNSDIR $WORKDIR $OUTDIR"
