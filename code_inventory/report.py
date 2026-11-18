from __future__ import annotations

from datetime import datetime
from pathlib import Path

import pandas as pd

from .config import COLUMNS
from .scanner import CodeFileScanner


class InventoryReport:
    """Un tableau par langage : un fichier de code par ligne."""

    def __init__(self, root: Path):
        self.root = root

    @property
    def code(self) -> str:
        return self.root.name

    def _row(self, path: Path) -> dict:
        stat = path.lstat()
        return {
            "Fichier": path.name,
            "Dossier": str(path.parent.relative_to(self.root)),  # "." si à la racine
            "Chemin": str(path),
            "Taille (Ko)": round(stat.st_size / 1024, 1),
            "Modifié le": datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M"),
        }

    def build(self) -> dict[str, pd.DataFrame]:
        scanner = CodeFileScanner(self.root)
        return {language: pd.DataFrame([self._row(p) for p in paths], columns=COLUMNS)
                for language, paths in scanner.files.items()}
