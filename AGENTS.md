# Repository Guidelines

## Project Structure & Module Organization
- `scripts/`: automation helpers (`import_pts.py` for `.dat`→`.geo`, `aoa_sweep.py` to clone `.ini` per AoA, `sweep.sh` orchestrates multi-AoA runs).
- `naca0012/`, `naca23012/`, `naca24012/`, `naca2412/`: each holds `mesh/` geometry/mesh, baseline `.ini`, solver-ready `.pbrm`, and per-AoA outputs (e.g., `aoa6/` or `runs/`).
- `results/`: notebooks for lift plots and ParaView states/exports; per-airfoil figures live in `results/<profile>/`.
- `fix_pvsm_paths.py`: utility to rewrite ParaView state files to relative paths when the repo moves.

## Build, Test, and Development Commands
- Regenerate mesh (run from repo root): `gmsh naca0012/mesh/naca0012.geo`.
- Convert mesh: `pybaram import naca0012/mesh/naca0012.msh naca0012/naca0012.pbrm`.
- Run solver: `pybaram run naca0012/naca0012.pbrm naca0012/naca0012.ini`.
- Export results: `pybaram export naca0012/naca0012.pbrm naca0012/aoa6/result.pbrs naca0012/aoa6/result.vtu`.
- AoA sweep (creates per-angle runs): `cd naca0012 && sh ../scripts/sweep.sh 0 18 2`.
- Convert airfoil points: `python scripts/import_pts.py naca0012/mesh/naca0012.dat naca0012/mesh/naca0012.geo True`.
- Normalize ParaView paths before sharing: `python fix_pvsm_paths.py`.

## Coding Style & Naming Conventions
- Python: 4-space indents, snake_case names, keep scripts dependency-light (numpy/stdlib). Favor explicit paths and small, composable functions. Keep profile names `nacaXXXX`; AoA directories `aoa<number>`.
- Shell: POSIX-compatible, parameterize paths; prefer relative paths so runs remain portable. Document non-default AoA ranges in comments.
- Notebooks: store rendered figures under `results/<profile>/`; avoid committing bulky intermediate solver outputs.

## Testing Guidelines
- No automated suite; validate changes by running a small AoA case end-to-end (`gmsh` → `pybaram import` → `pybaram run` → `pybaram export`) and opening the VTU in ParaView.
- For sweep changes, test with a narrow range (e.g., `sh ../scripts/sweep.sh 0 4 2`) and confirm directories populate with `.pbrs/.vtu`.
- When editing ParaView states, rerun `python fix_pvsm_paths.py` and reopen `results/contours.pvsm` to confirm paths resolve.

## Commit & Pull Request Guidelines
- Follow Conventional Commit prefixes seen here (`feat:`, `docs:`, `refactor:`); use short, imperative subjects and mention the airfoil/profile touched.
- PRs should include: summary of motivation, commands executed, before/after visuals or key metrics (e.g., updated `cl.png`), and noted dependencies (PyBaram/Gmsh versions, AoA range).
- Link related issues and avoid committing large raw solver datasets; keep reproducible scripts and configuration changes in-tree instead.

## Data & Configuration Tips
- When adding a new airfoil, clone an existing profile directory, update `.dat`/`.geo`, regenerate `.msh`/`.pbrm`, and keep `.ini` aligned with mesh resolution.
- Use `scripts/aoa_sweep.py` to generate AoA-specific `.ini` files rather than hand-editing; this keeps constants synchronized across runs.
