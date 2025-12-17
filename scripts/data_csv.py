from pymongo import MongoClient
import pandas as pd
from decimal import Decimal, InvalidOperation

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../.")))

from config.mongo_atlass import get_mongo_atlass_collection

# Récupérer la collection MongoDB
collection = get_mongo_atlass_collection("commandes")

rows = []

for doc in collection.find():
    produits = doc.get("produits", [])
    livraison = doc.get("livraison", {})
    for prod in produits:
        try:
            quantite = int(prod.get("quantite", 0))
        except (ValueError, TypeError):
            quantite = 0

        try:
            # Conversion explicite en Decimal, puis en float pour Power BI
            prix_unitaire = Decimal(str(prod.get("prix_unitaire", "0")).replace(",", "."))
        except (InvalidOperation, TypeError):
            prix_unitaire = 0.0

        rows.append({
            "ID Commande": doc.get("order_id"),
            "ID Client": doc.get("client_id"),
            "ID Produit": prod.get("produit_id"),
            "Nom Produit": prod.get("nom"),
            "Quantité": quantite,
            "Prix Unitaire": prix_unitaire,
            "Date Commande": doc.get("date_commande"),
            "Canal": doc.get("canal"),
            "Statut Commande": doc.get("statut_commande"),
            "Adresse Livraison": livraison.get("adresse", ""),
            "Ville Livraison": livraison.get("ville", "")
        })

# Création DataFrame
df = pd.DataFrame(rows)

# Formatage des types pour Power BI
df["Date Commande"] = pd.to_datetime(df["Date Commande"])

# Export CSV au format UTF-8 avec point comme séparateur décimal
df.to_csv("commandes.csv", index=False, encoding="utf-8", float_format="%.2f")

print("✅ Export terminé :", len(df), "lignes.")
