#!/bin/bash
#SBATCH --job-name=trainer                   	 # Job name
#SBATCH --output=%j_output.txt                   # Standard output file
#SBATCH --error=%j_error.txt                     # Standard error file
#SBATCH --ntasks=1                               # Number of tasks (usually = 1 for GPU jobs)
#SBATCH --cpus-per-task=4                        # Number of CPU cores per task (adjusted to 4)
#SBATCH --gres=gpu:1                             # Request 1 GPU
#SBATCH --mem=32G                                # Memory requested (32GB)
#SBATCH --time=1-00:00:00                        # Maximum time requested (1 days)
#SBATCH --partition=long                         # Partition name

python yolo.py
