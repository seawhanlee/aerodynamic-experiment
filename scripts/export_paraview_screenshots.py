#!/usr/bin/env pvpython
"""
Render ParaView state files (.pvsm) to PNG images for each AoA run.

Example:
    pvpython scripts/export_paraview_screenshots.py naca0012
"""

import argparse
from pathlib import Path
from typing import List, Optional, Tuple

# ParaView imports must come after standard library to keep linting happy.
from paraview.simple import (  # type: ignore
    GetLayout,
    GetSources,
    LoadState,
    Render,
    SaveScreenshot,
)


def collect_states(profile_dir: Path, runs_dir: str) -> List[Path]:
    """Return all .pvsm files under the runs directory for a profile."""
    search_root = profile_dir / runs_dir
    return sorted(search_root.rglob("*.pvsm"))


def find_vtu(run_dir: Path) -> Path:
    """Pick a VTU file that sits next to the state file in the run directory."""
    candidates = sorted(run_dir.glob("*.vtu"))
    if not candidates:
        raise FileNotFoundError(f"No .vtu found under {run_dir}")
    return candidates[0]


def assign_vtu_to_sources(vtu_path: Path) -> bool:
    """Force all sources with a FileName/FileNames attribute to use the VTU."""
    assigned = False
    for source in GetSources().values():
        if hasattr(source, "FileName"):
            source.FileName = [str(vtu_path)]
            assigned = True
        elif hasattr(source, "FileNames"):
            source.FileNames = [str(vtu_path)]
            assigned = True
    return assigned


def gather_views():
    """Return all views found in the current layout ordered by slot location."""
    layout = GetLayout()
    if not layout:
        return []

    # ParaView 6.x lacks layout.GetViews(); pull views from the proxy manager
    # and keep only those actually placed in the layout (location >= 0).
    from paraview import servermanager as sm  # type: ignore

    pm = sm.ProxyManager()
    raw_views = list(pm.GetProxiesInGroup("views").values())

    def view_location(view) -> int:
        try:
            return int(layout.GetViewLocation(view))
        except Exception:
            return -1

    return sorted(raw_views, key=view_location)


def classify_view(view) -> Optional[str]:
    """Guess view purpose from the active scalar (Cp or Speed)."""
    reps = getattr(view, "Representations", []) or []
    for rep in reps:
        if getattr(rep, "Visibility", 1) != 1:
            continue
        arr = getattr(rep, "ColorArrayName", None)
        if isinstance(arr, (list, tuple)) and arr:
            name = str(arr[-1]).lower()
        elif isinstance(arr, str):
            name = arr.lower()
        else:
            continue
        if "cp" in name:
            return "cp"
        if "speed" in name:
            return "speed"
    return None


def pick_resolution(view, override: Optional[Tuple[int, int]]) -> Tuple[int, int]:
    if override:
        return override
    view_size = getattr(view, "ViewSize", None)
    if isinstance(view_size, (list, tuple)) and len(view_size) == 2:
        return int(view_size[0]), int(view_size[1])
    return (1920, 1080)


def render_state(pvsm_path: Path, run_dir: Path, output_dir: Path, aoa_name: str, resolution: Optional[Tuple[int, int]]):
    vtu_path = find_vtu(run_dir)
    rel_state = pvsm_path.relative_to(Path.cwd()) if pvsm_path.is_absolute() else pvsm_path
    print(f"Rendering {rel_state}")

    LoadState(str(pvsm_path), data_directory=str(run_dir))
    assigned = assign_vtu_to_sources(vtu_path)
    if not assigned:
        print("  Warning: no sources accepted the VTU path; relying on paths in the state file.")

    views = gather_views()
    if not views:
        raise RuntimeError("No views found in the loaded state")

    output_dir.mkdir(parents=True, exist_ok=True)

    for idx, view in enumerate(views):
        tag = classify_view(view) or f"view{idx + 1}"
        image_path = output_dir / f"{aoa_name}_{tag}.png"
        Render()
        SaveScreenshot(
            str(image_path),
            viewOrLayout=view,
            ImageResolution=list(pick_resolution(view, resolution)),
        )
        print(f"  -> {image_path.relative_to(Path.cwd())}")



def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Export ParaView screenshots for AoA runs.")
    parser.add_argument("profile", help="Profile directory name (e.g., naca0012)")
    parser.add_argument(
        "--runs-dir",
        default="runs",
        help="Relative runs directory name under the profile (default: runs)",
    )
    parser.add_argument(
        "--resolution",
        nargs=2,
        type=int,
        metavar=("WIDTH", "HEIGHT"),
        default=None,
        help="Override screenshot resolution; defaults to the view size from the state.",
    )
    parser.add_argument(
        "--fallback-state",
        default="results/contours.pvsm",
        help="State file to use when a run directory lacks its own .pvsm (default: results/contours.pvsm).",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    repo_root = Path(__file__).resolve().parents[1]
    profile_dir = repo_root / args.profile
    if not profile_dir.exists():
        raise FileNotFoundError(f"Profile directory not found: {profile_dir}")

    runs_root = profile_dir / args.runs_dir
    run_dirs = sorted(p for p in runs_root.iterdir() if p.is_dir())
    if not run_dirs:
        raise SystemExit(f"No run directories found under {runs_root}")

    fallback_state = Path(args.fallback_state)
    if not fallback_state.is_absolute():
        fallback_state = repo_root / fallback_state
    if not fallback_state.exists():
        fallback_state = None

    output_dir = repo_root / "results" / profile_dir.name / "paraview"
    resolution = tuple(args.resolution) if args.resolution else None

    for run_dir in run_dirs:
        pvsm_candidates = sorted(run_dir.glob("*.pvsm"))
        if pvsm_candidates:
            pvsm_path = pvsm_candidates[0]
        elif fallback_state:
            pvsm_path = fallback_state
            print(f"Using fallback state for {run_dir.name}: {pvsm_path}")
        else:
            print(f"Skipping {run_dir.name}: no .pvsm and no fallback state available")
            continue

        try:
            render_state(pvsm_path, run_dir, output_dir, run_dir.name, resolution)
        except Exception as exc:
            print(f"✗ Failed on {run_dir.name}: {exc}")


if __name__ == "__main__":
    main()
