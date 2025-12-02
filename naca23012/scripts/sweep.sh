#!/bin/bash
# Please run on the parent folder
# Sweep AOA from 0 to 18 degrees (2 degree increments)

naca=naca23012

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
  python ../scripts/aoa_sweep.py $naca.ini $aoa.0 $naca.ini

  # Run CFD with local files
  pybaram run $naca.pbrm $naca.ini
  pybaram export $naca.pbrm out-10000.pbrs aoa$aoa.vtu
  
  # Create ParaView state file with correct AOA (in same directory as .vtu)
  sed -e "s|./aoa4.vtu|./aoa${aoa}.vtu|g" \
      -e "s|name=\"out.vtu\" logname=\"out.vtu\"|name=\"aoa${aoa}.vtu\" logname=\"aoa${aoa}.vtu\"|g" \
      ../results/contours.pvsm > ./contours.pvsm
  
  cd ..
  # Print blank line for readability between AOA runs
  echo
done

  echo "=========================================="
  echo "CFD complete"
  echo "=========================================="