# langage -> extensions (en minuscules)
LANGUAGES = {
    "R": (".r",),
    "Python": (".py",),
}

# dossiers ignorés pendant le parcours (environnements, caches, versionnage)
EXCLUDED_DIRS = {".git", "__pycache__", ".venv", "venv", "site-packages",
                 "node_modules", ".ipynb_checkpoints", "renv"}

COLUMNS = ["Fichier", "Dossier", "Chemin", "Taille (Ko)", "Modifié le"]
