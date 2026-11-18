from __future__ import annotations

import os
from functools import cached_property
from pathlib import Path

from .config import EXCLUDED_DIRS, LANGUAGES


class CodeFileScanner:
    """Parcourt un dossier racine (une seule fois) et classe les fichiers de code par langage."""

    def __init__(self, root: Path):
        self.root = root

    @staticmethod
    def _language(path: Path) -> str | None:
        suffix = path.suffix.lower()
        for language, extensions in LANGUAGES.items():
            if suffix in extensions:
                return language
        return None

    @cached_property
    def files(self) -> dict[str, list[Path]]:
        """Fichiers de code par langage, triés par chemin (dossiers exclus ignorés)."""
        found = {language: [] for language in LANGUAGES}
        for folder, subdirs, filenames in os.walk(self.root):
            subdirs[:] = [d for d in subdirs if d not in EXCLUDED_DIRS]
            for name in filenames:
                path = Path(folder) / name
                language = self._language(path)
                if language:
                    found[language].append(path)
        return {language: sorted(paths, key=lambda p: str(p).lower())
                for language, paths in found.items()}
