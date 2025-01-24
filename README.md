# DBT : Mini Projet ETL / Cloud Computing

## Contexte

Dans le cadre de ce mini-projet, nous nous attaquons à la construction d’un pipeline de données de bout en bout en utilisant un jeu de données brut. L’objectif principal est de développer un processus efficace de transformation de données pour répondre à des besoins analytiques spécifiques. Nous commencerons par examiner le schéma physique du jeu de données initial, qui nécessite une dénormalisation pour créer un schéma adapté à un DataWareHouse.

Le projet se concentrera sur l’utilisation de DBT (Data Build Tool) pour orchestrer les transformations de données et la création du schéma de l’entrepôt de données, qui sera hébergé sur Amazon Redshift. En travaillant avec ces technologies, nous visons à améliorer notre performance en SQL tout en approfondissant notre compréhension du data modeling. Ce projet est une opportunité d’appliquer les concepts de modélisation des données et de renforcer notre expertise en ingénierie des données, en nous assurant que notre pipeline est optimisé pour les besoins analytiques de l’organisation.

## Etapes clés

1. Data Modeling

    Analyser le jeu de données brut.  
    Concevoir le schéma physique des données.
    Déterminer les besoins de dénormalisation pour créer un schéma adapté au DataWareHouse.

2. Intégration des Données dans Redshift

    Mettre en place un entrepôt de données sur Amazon Redshift.
    Créer et configurer un cluster Redshift Serverless.
    Importer les données brutes dans Redshift.

3. Transformation des Données, Testing et Documentation à l'aide de DBT

    Utiliser DBT pour orchestrer les transformations de données.
    Créer des modèles DBT pour structurer les données selon le schéma dénormalisé.
    Effectuer des tests pour valider les transformations.
    Documenter les transformations et les modèles dans DBT.

4. Requêtes Analytiques

    Identifier les indicateurs clés de performance (KPI) pertinents.
    Écrire des requêtes SQL pour extraire des insights analytiques à partir des données transformées.
    Créer des rapports et des visualisations basés sur les résultats des requêtes analytiques à l'aide de librairies Python au choix.

## Présentation des données

Le jeu de données présenté ici provient d'une entreprise de vente au détail qui souhaite mieux comprendre ses opérations commerciales. Il contient des informations sur les clients, les produits, les commandes, les magasins, et les approvisionnements. Ce jeu de données permet de suivre plusieurs aspects clés du business, tels que :

- **Suivi des commandes clients** : Comprendre qui achète quoi, quand, et dans quel magasin.
- **Gestion des stocks** : Suivre les produits commandés et les niveaux d'approvisionnement en fonction des articles vendus et de leur disponibilité.
- **Analyse des performances des magasins** : Mesurer l'efficacité des magasins en fonction des commandes traitées, des ventes réalisées, et des taux de taxe appliqués.
- **Optimisation des coûts** : Évaluer les coûts des approvisionnements, particulièrement ceux des articles périssables, pour mieux gérer les marges.

L'objectif de l'entreprise est de mieux comprendre son activité afin de prendre des décisions plus éclairées en matière de gestion des stocks, d'optimisation des prix, et de maximisation des ventes.

---

### Détail des données

Voici les différentes tables et leurs colonnes respectives dans le jeu de données :

#### `raw_customers`
- **id** : Identifiant unique du client (integer).
- **name** : Nom du client (string).

#### `raw_items`
- **id** : Identifiant unique de l'article (integer).
- **order_id** : Identifiant de la commande à laquelle l'article appartient (integer).
- **sku** : Code de l'unité de gestion des stocks (stock keeping unit) pour l'article (string).

#### `raw_orders`
- **id** : Identifiant unique de la commande (integer).
- **customer_id** : Identifiant du client qui a passé la commande (integer).
- **ordered_at** : Date et heure de la commande (timestamp).
- **store_id** : Identifiant du magasin où la commande a été passée (integer).

#### `raw_products`
- **sku** : Code de l'unité de gestion des stocks pour le produit (string).
- **name** : Nom du produit (string).
- **type** : Type de produit (string).
- **price** : Prix du produit (decimal).
- **description** : Description du produit (text).

#### `raw_stores`
- **id** : Identifiant unique du magasin (integer).
- **name** : Nom du magasin (string).
- **opened_at** : Date et heure d'ouverture du magasin (timestamp).
- **tax_rate** : Taux de taxe applicable au magasin (decimal).

#### `raw_supplies`
- **id** : Identifiant unique de l'approvisionnement (integer).
- **name** : Nom de l'approvisionnement (string).
- **cost** : Coût de l'approvisionnement (decimal).
- **perishable** : Indique si l'approvisionnement est périssable (boolean).
- **sku** : Code de l'unité de gestion des stocks pour l'approvisionnement (string).

## Etape 1 : Data Modeling

**[Identification du schéma physique de la BDD opérationelle](./docs/schema_brut.png)**




