#!/bin/bash

# Restructure Datasets_IntensNormMethods.zip dataset into subjec layout

DATA_PATH="$HOME"/Data/Datasets_IntensNormMethods
DEST_PATH="$HOME"/Data/Datasets_IntensNormMethods_subjects

mkdir -p "$DATA_PATH" "$DEST_PATH"
unzip "$DATA_PATH"/activity_maps.zip -d "$DATA_PATH" 
unzip "$DATA_PATH"/attenuation_maps.zip -d "$DATA_PATH"
mv "$DATA_PATH"/attenuation_maps/* "$DATA_PATH"
rm -r "$DATA_PATH"/attenuation_maps "$DATA_PATH"/activity_maps.zip "$DATA_PATH"/attenuation_maps.zip

for f in "$DATA_PATH"/*; do
    filename="$(basename -- "$f")"
    subject="$(echo "$filename" | cut -d"_" -f1 | sed 's/S//')"
    maptype="$(echo "$filename" | cut -d"_" -f2)"
    dest_dir="$DEST_PATH"/DIN_"$subject"
    mkdir -p "$dest_dir"
    echo "$f" >> "$dest_dir"/metadata.txt
    mv "$f" "$dest_dir"/"$maptype"
done

rm -r "$DATA_PATH"
