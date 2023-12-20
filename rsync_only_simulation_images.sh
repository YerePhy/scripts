#!/bin/bash

SIMULATIONS="$HOME"/Data/Simulations
ONLY_IMAGES="$HOME"/Data/Simulations_images

rsync -rv \
    --exclude="*/division_*" \
    --include="*/" \
    --include="rec_*.img" \
    --include="rec_*.hdr" \
    --include="*.yaml" \
    --include="*/Maps/*" \
    --exclude="*" \
    "$SIMULATIONS" "$ONLY_IMAGES"
