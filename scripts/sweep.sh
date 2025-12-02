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
  echo "=========================================="
  echo "Running CFD for AOA = $aoa degrees"
  echo "=========================================="
  
  mkdir -p aoa$aoa
  cd aoa$aoa
  
  # Copy original .ini and .pbrm files
  cp ../$naca.ini $naca.ini
  cp ../$naca.pbrm $naca.pbrm
  
  # Edit AOA in the copied .ini file
  # We are in nacaXXXX/aoaXX, so scripts are in ../../scripts
  if [ -f "../../scripts/aoa_sweep.py" ]; then
      python ../../scripts/aoa_sweep.py $naca.ini $aoa.0 $naca.ini
  else
      echo "Error: ../../scripts/aoa_sweep.py not found."
      cd ..
      exit 1
  fi

  # Run CFD with local files
  pybaram run $naca.pbrm $naca.ini
  pybaram export $naca.pbrm out-10000.pbrs aoa$aoa.vtu

  # Create ParaView state file with correct AOA
  # Using ../../results/contours.pvsm because results are now in root
  if [ -f "../../results/contours.pvsm" ]; then
      sed -e "s|./aoa4.vtu|./aoa${aoa}.vtu|g" \
          -e "s|name=\"out.vtu\" logname=\"out.vtu\"|name=\"aoa${aoa}.vtu\" logname=\"aoa${aoa}.vtu\"|g" \
          ../../results/contours.pvsm > ./contours.pvsm
  fi
  
  cd ..
  echo
done

echo "=========================================="
echo "CFD complete for $naca"
echo "=========================================="
