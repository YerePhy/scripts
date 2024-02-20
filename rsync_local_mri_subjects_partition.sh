#!/bin/bash

ROOT_DATA="$HOME"/Data
ONLY_MRI_SUBJECTS="$ROOT_DATA"/subjects_with_mri
TMP="$ROOT_DATA"/tmp
DIRS=("first" "second" "third" "fourth")

#find "$SIMULATIONS_DATASET" -name "$MRI_FILE_NAME" -type f -exec dirname "{}" \; | xargs -I '{}' cp -rf '{}' "$ONLY_MRI_SUBJECTS" 
#mkdir -p "$TMP"/{first,second,third,fourth}


for subdir in "${DIRS[@]}"; do
    mkdir -p "$TMP"/"$subdir"
    find "$ONLY_MRI_SUBJECTS" -maxdepth 1 -type d |  grep -E '[0-9]+$' | head -25 | xargs -I '{}' mv '{}' "$TMP"/"$subdir"
done

mv "$TMP"/* "$ONLY_MRI_SUBJECTS"
rm -r "$TMP"


