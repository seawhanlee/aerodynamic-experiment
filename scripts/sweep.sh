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
  echo "=========================================="
  echo "Running CFD for AOA = $aoa degrees"
  echo "=========================================="
  
  mkdir -p runs/aoa$aoa
  cd runs/aoa$aoa
  
  # Copy original .ini and .pbrm files
  cp ../../$naca.ini $naca.ini
  cp ../../$naca.pbrm $naca.pbrm
  
  # Edit AOA in the copied .ini file
  # We are in nacaXXXX/runs/aoaXX, so scripts are in ../../../scripts
  if [ -f "../../../scripts/aoa_sweep.py" ]; then
      python ../../../scripts/aoa_sweep.py $naca.ini $aoa.0 $naca.ini
  else
      echo "Error: ../../../scripts/aoa_sweep.py not found."
      cd ../..
      exit 1
  fi

  # Run CFD with local files
  pybaram run $naca.pbrm $naca.ini
  
  # Find the last iteration file (converged or max iteration)
  last_pbrs=$(ls -v out-*.pbrs 2>/dev/null | tail -n 1)

  if [ -n "$last_pbrs" ]; then
      echo "Exporting result from $last_pbrs"
      pybaram export $naca.pbrm "$last_pbrs" aoa$aoa.vtu
  else
      echo "Error: No output .pbrs files found for AOA $aoa"
  fi

  # Create ParaView state file with correct AOA
  # Using ../../../results/contours.pvsm because results are now in root
  if [ -f "../../../results/contours.pvsm" ]; then
      sed -e "s|./aoa4.vtu|./aoa${aoa}.vtu|g" \
          -e "s|name=\"out.vtu\" logname=\"out.vtu\"|name=\"aoa${aoa}.vtu\" logname=\"aoa${aoa}.vtu\"|g" \
          ../../../results/contours.pvsm > ./contours.pvsm
  fi
  
  cd ../..
  echo
done

echo "=========================================="
echo "CFD complete for $naca"
echo "=========================================="

