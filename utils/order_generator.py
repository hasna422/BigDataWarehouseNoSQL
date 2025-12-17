import json
import os
import random
from faker import Faker
from datetime import datetime
import faker_commerce
from mimesis import Address
from mimesis.locales import Locale

# Initialisation des générateurs
fake = Faker()
fake.add_provider(faker_commerce.Provider)
address = Address(locale=Locale.EN)

def generate_products():
    return [
        {
            "produit_id": fake.unique.bothify(text="P####"),
            "nom": fake.unique.ecommerce_name(),
            "quantite": random.randint(1, 5),
            "prix_unitaire": round(random.uniform(5.0, 500.0), 2)
        }
        for _ in range(random.randint(1, 3))
    ]

def generate_address():
    """Génère une adresse complète avec ville en utilisant mimesis."""
    return {
        "adresse": f"{address.street_number()} {address.street_name()}",
        "ville": address.city()
    }

def generate_order(canal):
    livraison = generate_address() if canal in ["web", "mobile"] else None

    order = {
        "order_id": fake.unique.random_int(min=100000, max=999999),
        "client_id": fake.random_int(min=1000, max=9999),
        "produits": generate_products(),
        "date_commande": fake.date_time_between(start_date="-2y", end_date="now").isoformat(),
        "canal": canal,
        "statut_commande": random.choice(["payée", "annulée", "en attente"])
    }

    if livraison:
        order["livraison"] = livraison

    return order

def save_order_to_file(order, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    file_path = os.path.join(output_dir, f"{order['order_id']}.json")
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(order, f, indent=4, ensure_ascii=False)
    print(f"[{order['canal']}] Commande générée : {file_path}")
