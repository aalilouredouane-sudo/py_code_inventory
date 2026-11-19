# py_code_inventory

Python tool that lists the code files found under a root folder.

The code walks the folder recursively, classifies each file by language from its extension, and writes an Excel workbook with **one sheet per language** and **one row per file**:

- **Fichier**: file name;
- **Dossier**: parent folder, relative to the root (`.` for files at the root);
- **Chemin**: full path of the file;
- **Taille (Ko)**: size in kilobytes, rounded to one decimal;
- **Modifié le**: last modification date (`YYYY-MM-DD HH:MM`).

The languages currently covered are **R** (`.r`, `.R`) and **Python** (`.py`). Environment, cache and version-control folders are skipped.

---

## Folder structure

```
py_code_inventory/
├── main.py                  # entry point: run parameters and pipeline launch
├── requirements.txt         # dependencies (pandas, openpyxl)
├── README.md
└── code_inventory/          # inventory package
    ├── __init__.py          # classes exposed by the package
    ├── config.py            # constants (languages and extensions, excluded folders, output columns)
    ├── pipeline.py          # orchestration: checks, scan, console summary, export
    ├── scanner.py           # recursive walk of the root folder and classification by language
    ├── report.py            # one table per language, one row per file
    └── exporter.py          # Excel output (one sheet per language)
```

### Expected input

Any folder. Code files can be at any depth. For example:

```
<root>/
├── script.R                  # -> sheet R, Dossier = "."
├── projet_a/
│   ├── main.py               # -> sheet Python, Dossier = "projet_a"
│   ├── utils/
│   │   └── helpers.py        # -> sheet Python, Dossier = "projet_a/utils"
│   └── .venv/                # ignored (excluded folder)
└── projet_b/
    └── analyse.r             # -> sheet R, Dossier = "projet_b"
```

- The extension is compared case-insensitively: `.R` and `.r` are both R files.
- Folders whose name is in `EXCLUDED_DIRS` are not walked, at any depth: `.git`, `__pycache__`, `.venv`, `venv`, `site-packages`, `node_modules`, `.ipynb_checkpoints`, `renv`.
- Symbolic links to folders are not followed.

---

## User guide

1. **Install the dependencies.** Run `pip install -r requirements.txt`. `main.py` also installs any missing packages automatically at startup.
2. **Set the parameters** in [main.py](main.py):

   | Parameter | Purpose |
   |---|---|
   | `root` | Root folder to inventory. |
   | `output_path` | Path of the Excel file to create. If it already exists, it is overwritten. |

3. **Run the inventory**: `python main.py`. The console shows the number of files found per language, with a warning for any language with no file.
4. **Collect the output** at `output_path`:

   | Sheet | Content |
   |---|---|
   | `R` | One row per R file: `Fichier`, `Dossier`, `Chemin`, `Taille (Ko)`, `Modifié le`. |
   | `Python` | Same columns, for Python files. |

   Rows are sorted by full path, ignoring case. A language with no file still gets its sheet, with headers only. Column widths are adjusted to their content (capped at 80 characters).

5. **Add a language.** Add an entry to `LANGUAGES` in [config.py](code_inventory/config.py), for example `"SAS": (".sas",)`. Extensions must be lowercase and include the dot. A new sheet is created automatically.

---

## Code description

### `main.py`
Entry point. It checks that `pandas` and `openpyxl` are installed and installs any that are missing. It then builds a `CodeInventoryPipeline` with the run parameters and calls `.run()`.

### `code_inventory/config.py`
Global constants:
- `LANGUAGES`: language → tuple of lowercase extensions. The order of the dictionary sets the order of the sheets.
- `EXCLUDED_DIRS`: folder names skipped during the walk.
- `COLUMNS`: columns of each sheet, in order.

### `code_inventory/pipeline.py` — `CodeInventoryPipeline`
Orchestrates the full run:
- raises `FileNotFoundError` if `root` is not an existing folder;
- builds the tables with `InventoryReport`;
- prints the number of files per language, and a warning when a language has none;
- writes the workbook with `ExcelExporter`.

### `code_inventory/scanner.py` — `CodeFileScanner`
- `files` walks `root` once with `os.walk` (result cached) and returns, for each language of `LANGUAGES`, the list of matching paths. Excluded folders are removed from the walk, so their subfolders are not visited either.
- `_language` returns the language of a file from its lowercased extension, or `None` if the extension is not covered.
- Each list is sorted by full path, case-insensitively.

### `code_inventory/report.py` — `InventoryReport`
- `build` returns one `DataFrame` per language, with the columns of `COLUMNS` (an empty table if no file was found).
- `_row` builds the row of one file. The size and date come from `lstat`, so for a symbolic link they describe the link itself, not its target. `Dossier` is the parent folder relative to `root`.

### `code_inventory/exporter.py` — `ExcelExporter`
- `export` writes one sheet per language with `openpyxl`, without the index. Sheet names are truncated to 31 characters (Excel limit).
- Each column width is set to the longest value (or header) + 2, capped at 80.
