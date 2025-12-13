#!/usr/bin/env python

import numpy as np
import sys


def _concate_pts(n, i0=0):
    return ','.join(str(i) for i in range(i0, i0+n+1))


def main(ptsf, geof, is_spline=False):
    # Get pts
    pts = np.loadtxt(ptsf, skiprows=1)
    
    # Write geo file
    with open(geof, 'w') as f:
        # Write points
        for i, xi in enumerate(pts[:-1]):
            f.write('Point({}) = {{{},{}, 0.0, 1.0 }};\n'.format(i+1, *xi))

        if is_spline:
            # Write spline
            n =len(pts) // 2
            f.write("// airfoil spline\n")
            f.write("Spline({}) = {{{}}};\n".format(1, _concate_pts(n, 1)))
            f.write("Spline({}) = {{{}}};\n".format(2, _concate_pts(n-1,n+1)+',1'))


if __name__ == '__main__':
    # Parse arguments
    ptsf, geof = sys.argv[1], sys.argv[2]
    
    # Check is_spline argument
    try:
        is_spline = eval(sys.argv[3])
    except:
        is_spline = False
    
    main(ptsf, geof, is_spline)
