#!/bin/bash

SIMULATIONS_DATASET="$HOME"/Data/simulation_dataset
ONLY_MRI_SUBJECTS="$HOME"/Data/subjects_with_mri
MRI_FILE_NAME="resampled_T1.nii"


find "$SIMULATIONS_DATASET" -name "$MRI_FILE_NAME" -type f -exec dirname "{}" \; | xargs -I{} cp -rf {} "$ONLY_MRI_SUBJECTS" 
