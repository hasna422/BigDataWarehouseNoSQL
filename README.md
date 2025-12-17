
# 🛒 Mini-Projet Big Data Warehouse NoSQL – Simulation de flux de commandes multicanal
---

## 📌 Contexte général
La société **MultiMarket** opère plusieurs canaux de vente :
- Site web
- Application mobile
- Boutiques physiques

Chaque canal génère des commandes clients à différents moments de la journée.  
Dans un environnement réel, chaque canal produit un fichier JSON par commande.  

Le projet consiste à **simuler cet environnement**, collecter les commandes et construire un **Data Warehouse NoSQL** basé sur MongoDB.

---

## 🎯 Objectifs pédagogiques
- Simuler un flux de données hétérogène en provenance de différentes sources.  
- Gérer l’arrivée continue de données.  
- Construire un **Data Warehouse NoSQL** capable d’ingérer des commandes en continu.  
- Maîtriser l’analyse par agrégation sur des structures **semi-structurées (JSON / MongoDB)**.

---

## 🗂️ Structure du projet

```

MiniProjet-BigDataWarehouse/
│
├── data/
│   ├── sources/
│   │   ├── site_web/
│   │   ├── application_mobile/
│   │   └── boutique_physique/
│   ├── archive/
│
├── scripts/
│   ├── site_web.py
│   ├── application_mobile.py
│   ├── boutique_physique.py
│   └── collector.py
│
├── reports/
│   ├── mongodb_charts/
│   └── power_bi/
│
├── README.md
└── .gitignore

````

---

## 📝 Partie 1 – Simulation de la production de données
Chaque script Python (`site_web.py`, `application_mobile.py`, `boutique_physique.py`) :
- Génère une nouvelle commande au format JSON de manière aléatoire.  
- Dépose le fichier dans le répertoire spécifique :  
  - `/data/sources/site_web/`  
  - `/data/sources/application_mobile/`  
  - `/data/sources/boutique_physique/`  
- Génère une commande toutes les **2 à 5 secondes**.  

**Notes :**  
- Les commandes web et mobile contiennent une **adresse de livraison**.  
- Les commandes boutique n’ont pas d’adresse (achat sur place).  
- Volume minimum : **500 commandes par source**.

---

## 📝 Partie 2 – Collecte et intégration des données
Le script `collector.py` :
- Surveille en continu les répertoires `/data/sources/*/`.  
- Récupère chaque fichier JSON nouvellement arrivé.  
- Valide les données (format JSON correct).  
- Insère les commandes dans MongoDB (`multi_market`) dans la collection `commandes`.  
- Après traitement, déplace les fichiers vers `/data/archive/`.  

**Exigences techniques :**  
- Détection automatique des nouveaux fichiers  
- Traitement en **quasi temps réel** (max 10 secondes)  
- Robustesse : ignorer un fichier corrompu

---

## 📝 Partie 3 – Agrégation et analyse décisionnelle
Rapports MongoDB :
- Chiffre d'affaires total par **mois et par canal** (web, mobile, boutique)  
- **Top 10 produits** les plus vendus (en quantité)  
- **Taux de commandes annulées** par canal  
- Chiffre d'affaires moyen par commande pour chaque canal  

**Opérateurs MongoDB utilisés :**  
- `$group`  
- `$project`  
- `$match`  
- `$sort`

---

## 📝 Partie 4 – Reporting visuel
- Tableau de bord **MongoDB Charts** et **Power BI**  
- Visualisations incluses :  
  - Chiffre d'affaires total par mois et par canal  
  - Top 10 produits les plus vendus  
  - Taux de commandes annulées par canal  
  - Chiffre d'affaires moyen par commande

---

## 🛠️ Technologies utilisées
- Python 3.9+  
- MongoDB (NoSQL)  
- JSON  
- Faker
- Power BI  
- MongoDB Charts  

---

## 🚀 Lancement des scripts
1. **Simulateurs de commandes** :  
```bash
python scripts/site_web.py
python scripts/application_mobile.py
python scripts/boutique_physique.py
````

2. **Collecteur MongoDB** :

```bash
python scripts/collector.py
```

3. **Power BI / MongoDB Charts** :

* Ouvrir les fichiers `.pbix` ou configurer MongoDB Charts pour visualiser les rapports

---

