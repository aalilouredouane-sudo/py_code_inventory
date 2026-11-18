from __future__ import annotations

from pathlib import Path

from .report import InventoryReport
from .exporter import ExcelExporter


class CodeInventoryPipeline:
    def __init__(self, root: Path, output_path: Path):
        self.root = root
        self.output_path = output_path

    def run(self) -> None:
        if not self.root.is_dir():
            raise FileNotFoundError(f"Dossier introuvable : {self.root}")
        print(f"Scan de {self.root}")
        tables = InventoryReport(self.root).build()
        for language, table in tables.items():
            print(f"  {language} : {len(table)} fichier(s)")
            if table.empty:
                print(f"  [!] aucun fichier {language} trouvé")
        ExcelExporter(self.output_path).export(tables)
        print(f"Excel file created: {self.output_path}")
