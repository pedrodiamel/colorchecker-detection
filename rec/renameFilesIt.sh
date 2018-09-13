#!/bin/bash
EXT=png
FILES=./*.png
i=0
for f in $FILES
do
    echo "Processing $f file..."
    # take action on each file. $f store current file name
    mv $f frame-$i.$EXT
    i=`expr $i + 1`
done
