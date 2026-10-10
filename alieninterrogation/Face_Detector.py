"""Project-local launcher for the webcam emotion server.

GameMaker can run this file from inside the project tree, then request the
emotion data from the HTTP endpoint exposed by the repo-level detector.
"""

from pathlib import Path
import runpy
import sys

project_root = Path(__file__).resolve().parents[1]
target_script = project_root / "Face_Dectector.py"

if not target_script.exists():
    raise FileNotFoundError(f"Expected detector script at {target_script}")

if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

runpy.run_path(str(target_script), run_name="__main__")
