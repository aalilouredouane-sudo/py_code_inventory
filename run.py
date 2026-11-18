import importlib.util
import subprocess
import sys
from pathlib import Path

# module importable -> spécification pip
REQUIREMENTS = {
    "pandas": "pandas>=2.0",
    "openpyxl": "openpyxl>=3.1",
}


def ensure_dependencies() -> None:
    """Installe les packages manquants avant l'import du package code_inventory."""
    missing = [spec for mod, spec in REQUIREMENTS.items()
               if importlib.util.find_spec(mod) is None]
    if missing:
        subprocess.check_call([sys.executable, "-m", "pip", "install", *missing])


ensure_dependencies()

from code_inventory import CodeInventoryPipeline  # noqa: E402

if __name__ == "__main__":
    CodeInventoryPipeline(
        root=Path("chemin/vers/dossier"),
        output_path=Path("liste_codes.xlsx"),
    ).run()
