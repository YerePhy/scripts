#!/bin/bash

BIG_LESIONS="$HOME"/Data/Sujetos_simulados_con_lesiones_grandes_\(Sujetos_76_100\)
SMALL_LESIONS="$HOME"/Data/Sujetos_simulados_con_lesiones_pequeñas_\(Sujetos_1_75\)

create_metadata () {
    for dir in "$1"/*; do
        metadata_file="$dir"/metadata.txt
        if [ ! -f "$metadata_file" ]; then
            find "$dir" -type f >> "$metadata_file"
        fi
    done
}

rename_files_recursively () {
    find "$1" -type f -name "*$2*" -execdir mv '{}' "$3" \;
}

create_metadata "$BIG_LESIONS"
rename_files_recursively "$BIG_LESIONS" "Mapa_actividad" "actMap.nii"
rename_files_recursively "$BIG_LESIONS" "Mapa_atenuacion" "attMap.nii"

create_metadata "$SMALL_LESIONS"
rename_files_recursively "$SMALL_LESIONS" "Mapa_actividad" "actMap.nii"
rename_files_recursively "$SMALL_LESIONS" "Mapa_atenuacion" "attMap.nii"


