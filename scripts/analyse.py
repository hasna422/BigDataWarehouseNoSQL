import os
from pprint import pprint
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../.")))

from config.mongo_atlass import get_mongo_atlass_collection

# Récupérer la collection MongoDB
collection = get_mongo_atlass_collection("commandes")

#✅ 1. Chiffre d'affaires total par mois et par canal

pipeline_ca_mensuel = [
    {
        "$unwind": "$produits"
    },
    {
        "$group": {
            "_id": {
                "mois": { "$substr": ["$date_commande", 0, 7] },
                "canal": "$canal"
            },
            "total_ca": {
                "$sum": { "$multiply": ["$produits.quantite", "$produits.prix_unitaire"] }
            }
        }
    },
    { "$sort": { "_id.mois": 1, "_id.canal": 1 } }
]

print("📊 Chiffre d'affaires total par mois et par canal :")
pprint(list(collection.aggregate(pipeline_ca_mensuel)))

# ✅ 2. Top 10 des produits les plus vendus (par quantité)

pipeline_top_produits = [
    { "$unwind": "$produits" },
    {
        "$group": {
            "_id": "$produits.nom",
            "total_vendu": { "$sum": "$produits.quantite" }
        }
    },
    { "$sort": { "total_vendu": -1 } },
    { "$limit": 10 }
]

print("\n🏆 Top 10 des produits les plus vendus :")
pprint(list(collection.aggregate(pipeline_top_produits)))

#✅ 3. Taux de commandes annulées par canal
pipeline_annulations = [
    {
        "$group": {
            "_id": "$canal",
            "total": { "$sum": 1 },
            "annulees": {
                "$sum": {
                    "$cond": [{ "$eq": ["$statut_commande", "annulée"] }, 1, 0]
                }
            }
        }
    },
    {
        "$project": {
            "canal": "$_id",
            "_id": 0,
            "taux_annulation": {
                "$round": [{ "$multiply": [{ "$divide": ["$annulees", "$total"] }, 100] }, 2]
            }
        }
    }
]

print("\n🚫 Taux de commandes annulées par canal :")
pprint(list(collection.aggregate(pipeline_annulations)))

#✅ 4. Chiffre d'affaires moyen par commande (par canal)

pipeline_ca_moyen = [
    { "$unwind": "$produits" },
    {
        "$group": {
            "_id": "$order_id",
            "canal": { "$first": "$canal" },
            "ca_commande": {
                "$sum": { "$multiply": ["$produits.quantite", "$produits.prix_unitaire"] }
            }
        }
    },
    {
        "$group": {
            "_id": "$canal",
            "moyenne_ca": { "$avg": "$ca_commande" }
        }
    },
    {
        "$project": {
            "canal": "$_id",
            "_id": 0,
            "moyenne_ca": { "$round": ["$moyenne_ca", 2] }
        }
    }
]

print("\n💰 Chiffre d'affaires moyen par commande (par canal) :")
pprint(list(collection.aggregate(pipeline_ca_moyen)))

