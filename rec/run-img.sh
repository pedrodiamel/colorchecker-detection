#!/bin/bash
FILES=./db/*.jpg
i=0
for f in $FILES
do
    echo "Processing $f file..."
    # take action on each file. $f store current file name
    MCC.exe $f -o=./out -t=1 -nc=2 -gt -sh
    i=`expr $i + 1`
done
