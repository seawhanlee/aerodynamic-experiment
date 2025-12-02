#!/bin/bash
# Please run on the parent folder

for aoa in 0 2 4 6 8 12 16
do
  mkdir aoa$aoa
  cd aoa$aoa
  python ../scripts/aoa_sweep.py ../naca2412.ini $aoa.0 naca2412.ini 
  pybaram run ../naca2412.pbrm naca2412.ini
  cd ..
done
