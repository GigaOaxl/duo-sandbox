import sys
from pathlib import Path

# src-Layout ohne Installation: "python3 -m unittest" im Wurzelordner findet sandbox hier.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
