# Project: Aerodynamic Experiment (NACA Airfoils)

## Overview
This project performs subsonic inviscid flow analysis on various NACA airfoils (e.g., NACA 0012, NACA 23012, NACA 2412). It utilizes `gmsh` for mesh generation, `pybaram` for Computational Fluid Dynamics (CFD) simulations, and `paraview` for visualization.

## Prerequisites
The following tools are required to run the simulations and visualizations:
*   **Gmsh:** Mesh generator.
*   **PyBaram:** CFD solver.
*   **ParaView:** Data visualization application.
*   **Python 3:** With `numpy` installed (required for scripts).

## 📁 디렉토리 구조

이 저장소는 원본 시뮬레이션 데이터와 스크립트 및 결과를 분리하여 구성되었습니다:

```text
.
├── fix_pvsm_paths.py   # ParaView 상태 파일(.pvsm) 경로 수정 유틸리티
├── scripts/            # 자동화를 위한 중앙 스크립트 (AoA 스윕, 격자 가져오기 등)
├── results/            # 분석용 노트북 및 중앙 가시화 상태 파일
│   ├── naca0012/       # NACA 0012에 대한 출력 이미지/플롯
│   ├── naca23012/      # NACA 23012에 대한 출력 이미지/플롯
│   └── ...
├── naca0012/           # NACA 0012 시뮬레이션 디렉토리
│   ├── mesh/           # 형상(.geo) 및 격자(.msh) 파일
│   ├── runs/           # (생성됨) 모든 시뮬레이션 실행 결과가 여기에 저장됨
│   │   └── aoaX/       # 특정 받음각 시뮬레이션에 대한 출력
│   ├── naca0012.ini    # PyBaram 기본 설정 파일
│   └── naca0012.pbrm   # PyBaram 격자 파일
├── naca23012/          # NACA 23012 시뮬레이션 디렉토리
└── ...
```

## Usage

### 1. Mesh Generation & Import
To prepare the mesh for a simulation (example for `naca0012`):

```bash
# 1. Generate mesh using Gmsh
gmsh mesh/naca0012.geo

# 2. Import mesh to PyBaram format
pybaram import mesh/naca0012.msh naca0012.pbrm
```

### 2. Running a Single Simulation
To run a single simulation with the default configuration:

```bash
# Run the solver
pybaram run naca0012.pbrm naca0012.ini

# Export results to VTU format for ParaView
pybaram export naca0012.pbrm out-10000.pbrs output.vtu
```

### 3. Running an Angle of Attack (AoA) Sweep
To automatically run simulations for a range of AoAs (0, 2, ..., 18 degrees):

    ```bash
    sh ../scripts/sweep.sh          # 기본 범위 (0, 2, ..., 18도)
    sh ../scripts/sweep.sh 0 20 2   # 0도에서 20도까지 2도 증분으로 실행
    sh ../scripts/sweep.sh 5 15 1   # 5도에서 15도까지 1도 증분으로 실행
    ```
    *이 스크립트는 자동으로 `runs/` 디렉토리를 생성하고 그 안에 `aoaX` 폴더를 만듭니다. 각 각도에 대해 솔버를 실행하며, VTU 파일을 내보냅니다.*

### 4. Visualization
Visualize the results using ParaView:

```bash
# Load a pre-configured state file
paraview --state=results/contours.pvsm
```

### 5. Analysis
The `results/` directory contains analysis scripts and stores output images for each profile.
*   `results/plot_CL_py.ipynb`: Python notebook to plot Lift Coefficient (CL) vs Angle of Attack.
    *   **Usage:** Open the notebook, set the `profile` variable (e.g., `'naca0012'`, `'naca23012'`) in the first cell, and run all cells.
    *   **Output:** Saves `cl.png` to the respective profile folder (e.g., `results/naca0012/cl.png`).

## Scripts
*   `scripts/import_pts.py`: Root-level script to convert point data files into Gmsh `.geo` files with spline definitions.
    *   Usage: `python scripts/import_pts.py <points_file> <output_geo_file> [is_spline]`
*   `scripts/aoa_sweep.py`: Helper script used by `sweep.sh` to modify the `aoa` parameter in `.ini` files programmatically.
*   `scripts/sweep.sh`: Shell script to orchestrate the AoA sweep process. Run this from the airfoil directory.

## Development Guidelines
*   **Commit Messages:**
    *   Always write commit message in Korean.
    *   Must follow the standard format: `<type>: <description>` (e.g., `feat: 새로운 기능 추가`, `fix: 버그 수정`).
