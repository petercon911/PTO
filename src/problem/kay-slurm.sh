#!/bin/sh

#SBATCH --time=10:00:00
#SBATCH --nodes=1
#SBATCH -A nuig02
#SBATCH -p ProdQ
#SBATCH --mail-user=p.conway9@nuigalway.ie
#SBATCH --mail-type=BEGIN,END


# run this on login node with sbatch kay-slurm.sh

module load taskfarm
module load conda/2
#source activate myenv

cd $SLURM_SUBMIT_DIR
taskfarm run_exp.sh