#!/bin/bash
 
BASE_DIR="$(pwd)"
 
echo "Base directory: $BASE_DIR"
echo "Processing ALL folders in the current directory..."
 
for d in */ ; do
    # Remove trailing slash
    d=${d%/}
 
    # Skip if not a directory
    if [ ! -d "$d" ]; then
        continue
    fi
 
    # Skip FRCM.py itself
    if [ "$d" = "FRCM.py" ]; then
        continue
    fi
 
    echo "Processing folder: $d"
 
    # 3. Run FRCM.py inside the folder with nohup
    (
        cd "$BASE_DIR/$d" || exit
        nohup python3 FRCM.py > evaluation.txt 2>&1 &
    )
done
 
echo "All tasks launched."