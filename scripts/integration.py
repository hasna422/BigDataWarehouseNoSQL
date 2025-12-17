import os
import json
import shutil
import time
from pathlib import Path
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../.")))

from config.mongo_atlass import get_mongo_atlass_collection

# Récupérer la collection MongoDB
collection = get_mongo_atlass_collection("commandes")

# Dossiers
BASE_SOURCE_DIR = Path("data/sources")
ARCHIVE_DIR = Path("data/archive")
ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)

def validate_json_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Validation de base
        assert all(key in data for key in ["order_id", "client_id", "produits", "date_commande", "canal", "statut_commande"])
        return data

    except Exception as e:
        print(f"[ERREUR] Fichier invalide {filepath.name} : {e}")
        return None

def archive_file(filepath):
    dest = ARCHIVE_DIR / filepath.name
    shutil.move(str(filepath), dest)

def process_files():
    for source_dir in BASE_SOURCE_DIR.iterdir():
        if source_dir.is_dir():
            for file in source_dir.glob("*.json"):
                data = validate_json_file(file)
                if data:
                    try:
                        collection.insert_one(data)
                        print(f"[OK] {file.name} insérée depuis canal '{data['canal']}'")
                    except Exception as e:
                        print(f"[ERREUR] Insertion MongoDB échouée pour {file.name} : {e}")
                archive_file(file)

if __name__ == "__main__":
    print("🔁 Collecteur MongoDB en cours d’exécution (toutes les 10 sec)...")
    while True:
        process_files()
        time.sleep(10)
