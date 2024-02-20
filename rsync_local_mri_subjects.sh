#!/bin/bash

SIMULATIONS_DATASET="$HOME"/Data/simulation_dataset
ONLY_MRI_SUBJECTS="$HOME"/Data/subjects_with_mri
MRI_FILE_NAME="resampled_T1.nii"


find "$SIMULATIONS_DATASET" -name "$MRI_FILE_NAME" -type f -exec dirname "{}" \; | xargs -I{} cp -rf {} "$ONLY_MRI_SUBJECTS" 
mkdir -p "$ONLY_MRI_SUBJECTS"/51
find "$ONLY_MRI_SUBJECTS" -maxdepth 1 -type f -exec mv {} "$ONLY_MRI_SUBJECTS"/51 \;
