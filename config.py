from pathlib import Path
APP_NAME="Fuhrpark-Kostenkontrolle"
NETWORK_DIR=Path(r"R:\Disposition\Fuhrpark_Kostenkontrolle")
LOCAL_DIR=Path(__file__).resolve().parent/"data"
DATA_DIR=NETWORK_DIR if NETWORK_DIR.exists() else LOCAL_DIR
DATA_DIR.mkdir(parents=True,exist_ok=True)
DATABASE_PATH=DATA_DIR/"fuhrpark.db"
COLORS={"orange":"#F28C00","blau":"#17365D","hell":"#F5F6F7"}
from pathlib import Path

APP_NAME = "Fuhrpark-Kostenkontrolle"

# Netzwerkpfad (Produktiv)
NETWORK_DIR = Path(r"R:\Disposition\Fuhrpark_Kostenkontrolle")

# Lokaler Fallback
LOCAL_DIR = Path(__file__).resolve().parent / "data"

# Datenordner bestimmen
DATA_DIR = NETWORK_DIR if NETWORK_DIR.exists() else LOCAL_DIR
DATA_DIR.mkdir(parents=True, exist_ok=True)

# Unterordner
BACKUP_DIR = DATA_DIR / "Backups"
EXPORT_DIR = DATA_DIR / "Exporte"
LOG_DIR = DATA_DIR / "Logs"

for ordner in [BACKUP_DIR, EXPORT_DIR, LOG_DIR]:
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