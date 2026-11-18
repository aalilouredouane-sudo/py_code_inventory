from __future__ import annotations

from pathlib import Path

import pandas as pd
from openpyxl.utils import get_column_letter


class ExcelExporter:
    """Écrit un classeur : une feuille par langage."""

    def __init__(self, output_path: Path):
        self.output_path = output_path

    def export(self, tables: dict[str, pd.DataFrame]) -> None:
        with pd.ExcelWriter(self.output_path, engine="openpyxl") as writer:
            for language, table in tables.items():
                table.to_excel(writer, sheet_name=language[:31], index=False)
                sheet = writer.sheets[language[:31]]
                for i, column in enumerate(table.columns, start=1):
                    width = max([len(str(column))] + [len(str(v)) for v in table[column]]) + 2
                    sheet.column_dimensions[get_column_letter(i)].width = min(width, 80)
