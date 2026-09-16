from pathlib import Path

APP_NAME = "Fuhrpark-Kostenkontrolle"

# Firmenpfad
NETWORK_DIR = Path(r"R:\Disposition\Fuhrpark_Kostenkontrolle")

# Fallback für Entwicklung
LOCAL_DIR = Path(__file__).resolve().parent / "data"

# Prüfen, ob Netzlaufwerk verfügbar ist
if NETWORK_DIR.exists():
    DATA_DIR = NETWORK_DIR
else:
    DATA_DIR = LOCAL_DIR

DATA_DIR.mkdir(parents=True, exist_ok=True)

# Unterordner automatisch anlegen
BACKUP_DIR = DATA_DIR / "Backups"
EXPORT_DIR = DATA_DIR / "Exporte"
LOG_DIR = DATA_DIR / "Logs"
SETTINGS_DIR = DATA_DIR / "Einstellungen"

for ordner in [BACKUP_DIR, EXPORT_DIR, LOG_DIR, SETTINGS_DIR]:
    ordner.mkdir(exist_ok=True)

DATABASE_PATH = DATA_DIR / "fuhrpark.db"

COLORS = {
    "orange": "#F28C00",
    "blau": "#17365D",
    "hell": "#F5F6F7",
    "weiß": "#FFFFFF",
    "grün": "#2E8B57",
    "rot": "#C0392B",
    "gelb": "#F1C40F",
}