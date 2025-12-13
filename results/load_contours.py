#!/usr/bin/env pvpython
"""
ParaView Python script to load any VTU file and apply contour visualization.

Usage:
    pvpython load_contours.py <vtu_file>
    
Or in ParaView GUI:
    Tools > Python Shell > Run Script
"""

import sys
import os
import glob
from paraview.simple import *

def find_vtu_file(directory="."):
    """Find a VTU file in the specified directory."""
    vtu_files = glob.glob(os.path.join(directory, "*.vtu"))
    if vtu_files:
        return vtu_files[0]
    return None

def setup_visualization(vtu_path):
    """Set up the contour visualization for a VTU file."""
    
    # Load VTU file
    print(f"Loading: {vtu_path}")
    reader = XMLUnstructuredGridReader(FileName=[vtu_path])
    reader.CellArrayStatus = ['Density', 'Pressure', 'Velocity']
    
    # Convert cell data to point data for smoother visualization
    cellToPoint = CellDatatoPointData(Input=reader)
    cellToPoint.ProcessAllArrays = 1
    
    # Calculate Cp (pressure coefficient)
    # Cp = (P - P_inf) / (0.5 * rho_inf * V_inf^2)
    # Assuming: P_inf = 101325 Pa, rho_inf = 1.225 kg/m³, V_inf = 50 m/s
    calculator = Calculator(Input=cellToPoint)
    calculator.ResultArrayName = 'Cp'
    calculator.Function = '(Pressure - 101325) / (0.5 * 1.225 * 50 * 50)'
    
    # Create contour for Cp
    contour = Contour(Input=calculator)
    contour.ContourBy = ['POINTS', 'Cp']
    contour.Isosurfaces = [-2.0, -1.5, -1.0, -0.5, 0.0, 0.5, 1.0]
    
    # Get active view or create new one
    renderView = GetActiveViewOrCreate('RenderView')
    
    # Show the original data with Cp coloring
    display = Show(calculator, renderView)
    display.Representation = 'Surface'
    ColorBy(display, ('POINTS', 'Cp'))
    
    # Set up color map
    cpLUT = GetColorTransferFunction('Cp')
    cpLUT.RescaleTransferFunction(-2.0, 1.0)
    
    # Show contour lines
    contourDisplay = Show(contour, renderView)
    contourDisplay.Representation = 'Surface'
    contourDisplay.AmbientColor = [0.0, 0.0, 0.0]
    contourDisplay.DiffuseColor = [0.0, 0.0, 0.0]
    
    # Show color bar
    cpLUTColorBar = GetScalarBar(cpLUT, renderView)
    cpLUTColorBar.Title = 'Cp'
    cpLUTColorBar.Visibility = 1
    
    # Reset camera to fit data
    renderView.ResetCamera()
    
    # Render
    Render()
    
    print("Visualization setup complete!")
    return reader, calculator, contour

def main():
    # Get VTU file from command line or find in current directory
    if len(sys.argv) > 1:
        vtu_path = sys.argv[1]
    else:
        # Try to find a VTU file in current directory
        vtu_path = find_vtu_file(".")
        if not vtu_path:
            print("Usage: pvpython load_contours.py <vtu_file>")
            print("Or place a .vtu file in the current directory.")
            sys.exit(1)
    
    if not os.path.exists(vtu_path):
        print(f"Error: File not found: {vtu_path}")
        sys.exit(1)
    
    setup_visualization(vtu_path)

if __name__ == "__main__":
    main()
