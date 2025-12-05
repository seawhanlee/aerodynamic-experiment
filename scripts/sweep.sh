#!/bin/bash
# Sweep AOA from 0 to 18 degrees (2 degree increments)
# Usage: Run this script from the profile directory (e.g., cd naca0012 && sh ../scripts/sweep.sh [start_aoa] [end_aoa] [aoa_increment])

# Detect profile name from the current directory name
naca=$(basename "$PWD")

echo "Detected profile: $naca"
if [ ! -f "$naca.ini" ]; then
    echo "Error: $naca.ini not found in current directory."
    exit 1
fi

# Set default AOA range
start_aoa=0
end_aoa=18
aoa_increment=2

# Override defaults with command-line arguments if provided
if [ -n "$1" ]; then
    start_aoa=$1
fi
if [ -n "$2" ]; then
    end_aoa=$2
fi
if [ -n "$3" ]; then
    aoa_increment=$3
fi

echo "Running AOA sweep from $start_aoa to $end_aoa with increment $aoa_increment"

# Create runs directory if it doesn't exist
mkdir -p runs

for aoa in $(seq $start_aoa $aoa_increment $end_aoa)
do
  echo "==========================================