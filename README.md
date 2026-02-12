# Django Shop - Clean Architecture avec Service Layer

Projet Django démontrant une architecture avec séparation des responsabilités :
- **Views** : gestion HTTP uniquement
- **Service** : logique métier encapsulée
- Gestion transparente session/DB selon l'authentification utilisateur

## Installation

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Utilisation

1. Ajouter des produits via l'interface admin (`/admin/`)
2. Consulter les produits sur la page d'accueil (`/`)
3. Ajouter des articles au panier (authentifié ou non)
4. Consulter le panier (`/cart/`)

## Comportement selon l'authentification

**Utilisateur authentifié :**
- Panier persistant en base de données (modèles Cart/CartItem)
- Stock décrémenté automatiquement
- Conservation du panier entre sessions

**Utilisateur anonyme :**
- Panier stocké en session
- Stock non modifié
- Panier temporaire

## Architecture

```
cart/
├── models.py          # Modèles Cart et CartItem
├── cart_service.py    # CartService - logique métier
└── views.py           # Vues minimalistes
shop/
├── models.py          # Modèle Product
└── views.py           # Vue index
templates/             # Templates avec Simple.css
```

## Service Layer Pattern

### CartService

```python
cart_service = CartService(request)
cart_service.add_item(product, quantity)
items = cart_service.get_items()
total = cart_service.get_total()
cart_service.clear()
```

**Avantages :**
- Séparation des responsabilités
- Testabilité accrue
- Maintenabilité du code
- Réutilisabilité (API, CLI, etc.)
- Abstraction de l'état d'authentification

## Principes démontrés

- Service Layer Pattern
- Encapsulation de la logique métier
- Abstraction des sources de données
- Single Responsibility Principle
- DRY (Don't Repeat Yourself)
