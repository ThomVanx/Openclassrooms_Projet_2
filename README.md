# Books to Scrape — Scraper

Scraper Python permettant d'extraire les données de tous les livres du site [Books to Scrape](https://books.toscrape.com), organisées par catégorie.

## Fonctionnalités

- Extraction des informations de chaque livre (titre, prix, note, description, disponibilité...)
- Export des données en fichiers CSV par catégorie
- Téléchargement des couvertures de livres, organisées par catégorie
- Gestion automatique de la pagination

## Données extraites

| Champ | Description |
|---|---|
| `product_page_url` | URL de la page du livre |
| `universal_product_code` | Code UPC du livre |
| `title` | Titre |
| `price_including_tax` | Prix TTC |
| `price_excluding_tax` | Prix HT |
| `number_available` | Stock disponible |
| `product_description` | Description |
| `category` | Catégorie |
| `review_rating` | Note (x/5) |
| `image_url` | URL de la couverture |

## Structure des fichiers générés

```
output/
├── fiction.csv
├── science.csv
└── ...
output_image/
├── fiction/
│   ├── book1.jpg
│   └── ...
├── science/
│   └── ...
```

## Installation

### Prérequis

- Python 3.x
- Git

### 1. Cloner le repository

```bash
git clone https://github.com/votre-username/votre-repo.git
cd votre-repo
```

### 2. Créer et activer l'environnement virtuel

**Windows (PowerShell) :**
```powershell
python -m venv env
env\Scripts\activate
```

**Mac/Linux :**
```bash
python3 -m venv env
source env/bin/activate
```

> Une fois activé, vous devriez voir `(env)` au début de votre ligne de commande.

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

## Utilisation

```bash
python main.py
```

Le script affiche la progression en temps réel :

```
Begin Extraction
Fiction - Extracting
Fiction - Extraction finished
Science - Extracting
...
All extractions finished
```

Les fichiers CSV et les images sont générés dans les dossiers `output/` et `output_image/`.

## Dépendances

- [requests](https://requests.readthedocs.io/) — requêtes HTTP
- [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/) — parsing HTML
