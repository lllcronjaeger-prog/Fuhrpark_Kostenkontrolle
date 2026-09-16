from pathlib import Path
APP_NAME="Fuhrpark-Kostenkontrolle"
NETWORK_DIR=Path(r"R:\Disposition\Fuhrpark_Kostenkontrolle")
LOCAL_DIR=Path(__file__).resolve().parent/"data"
DATA_DIR=NETWORK_DIR if NETWORK_DIR.exists() else LOCAL_DIR
DATA_DIR.mkdir(parents=True,exist_ok=True)
DATABASE_PATH=DATA_DIR/"fuhrpark.db"
COLORS={"orange":"#F28C00","blau":"#17365D","hell":"#F5F6F7"}
