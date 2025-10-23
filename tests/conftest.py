import sys
from pathlib import Path

# Adiciona o src ao sys.path para que imports absolutos funcionem
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
