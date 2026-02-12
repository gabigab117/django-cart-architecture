# Shop Example - Legacy Code Pattern

Projet de démonstration illustrant la différence entre une architecture legacy (logique métier dans les vues) et une architecture structurée avec services.

## Installation

```bash
# Migrations
python manage.py makemigrations
python manage.py migrate

# Créer un superuser
python manage.py createsuperuser

# Lancer le serveur
python manage.py runserver
```

## Utilisation

1. Ajouter des produits via l'interface d'administration `/admin/`
2. Consulter le catalogue sur `/`
3. Ajouter des produits au panier (authentifié ou anonyme)
4. Consulter le panier sur `/cart/`

## Comportement selon l'authentification

**Utilisateur authentifié** : panier persistant en base de données (Cart/CartItem), décrémentation automatique du stock

**Utilisateur anonyme** : panier temporaire en session, stock inchangé

## Structure du projet

- `shop/models.py` - Modèle Product
- `cart/models.py` - Modèles Cart et CartItem
- `shop/views.py` - Logique métier dans les vues (pattern legacy)
- `templates/` - Templates avec Simple.css

## Refactoring proposé

Extraction de la logique métier dans un `CartService` pour respecter le principe de responsabilité unique (SRP).
