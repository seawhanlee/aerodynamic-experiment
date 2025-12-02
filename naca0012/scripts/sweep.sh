#!/bin/bash
# Please run on the parent folder
# Sweep AOA from 0 to 18 degrees (2 degree increments)

for aoa in 0 2 4 6 8 10 12 14 16 18
do
  echo "=========================================="
  echo "Running CFD for AOA = $aoa degrees"
  echo "=========================================="
  
  mkdir -p aoa$aoa
  cd aoa$aoa
  
  # Copy original .ini and .pbrm files
  cp ../naca0012.ini naca0012.ini
  cp ../naca0012.pbrm naca0012.pbrm
  
  # Edit AOA in the copied .ini file
  python ../scripts/aoa_sweep.py naca0012.ini $aoa.0 naca0012.ini
  
  # Run CFD with local files
  pybaram run naca0012.pbrm naca0012.ini
  pybaram export naca0012.pbrm out-10000.pbrs aoa$aoa.vtu

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