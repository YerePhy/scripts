#!/bin/bash

while true; do 
    sudo sh -c 'echo 1 >  /proc/sys/vm/drop_caches';
    echo "Cache dropped.";
    sleep 50m;
done
