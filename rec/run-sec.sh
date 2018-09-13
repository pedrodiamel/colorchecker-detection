#!/bin/bash
echo "Processing file..."
 # sequence image file
MCC.exe ./db/frame-0.jpg -o=./out -sh -t=3 -nc=2 -me=2.0 -gt
