#!/bin/bash
# Sweep AOA from 0 to 18 degrees (2 degree increments)
# Usage: Run this script from the profile directory (e.g., cd naca0012 && sh ../scripts/sweep.sh)

# Detect profile name from the current directory name
naca=$(basename "$PWD")

echo "Detected profile: $naca"
if [ ! -f "$naca.ini" ]; then
    echo "Error: $naca.ini not found in current directory."
    exit 1
fi

for aoa in 0 2 4 6 8 10 12 14 16 18
do
  echo "==========================================