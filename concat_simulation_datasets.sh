#!/bin/bash

INTENSITY_NORM="$HOME"/Data/Datasets_IntensNormMethods_subjects
BIG_LESIONS="$HOME"/Data/Sujetos_simulados_con_lesiones_pequeñas_\(Sujetos_1_75\)
SMALL_LESIONS="$HOME"/Data/Sujetos_simulados_con_lesiones_grandes_\(Sujetos_76_100\)
DEST_DIR="$HOME"/Data/simulation_dataset

mkdir -p "$DEST_DIR"
mv "$INTENSITY_NORM"/* "$BIG_LESIONS"/* "$SMALL_LESIONS"/* "$DEST_DIR"

counter=0
for dir in "$DEST_DIR"/*; do
    mv "$dir" "$DEST_DIR"/"$counter"
    ((counter++))
done


