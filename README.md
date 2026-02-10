# 🛍️ Shop Example - Version CLEAN avec Service Layer

Projet Django démontrant une architecture propre avec séparation des responsabilités : 
- **Vues** : gestion HTTP uniquement
- **Service** : toute la logique métier encapsulée
- Gestion transparente session/DB selon authentification

## 🚀 Démarrage rapide

```bash
# Migrations
python manage.py makemigrations
python manage.py migrate

# Créer un superuser
python manage.py createsuperuser

# Lancer le serveur
python manage.py runserver
```

## 📋 Utilisation

1. **Ajouter des produits** via `/admin/`
2. **Voir les produits** sur la page d'accueil `/`
3. **Ajouter au panier** (fonctionne connecté ou non)
4. **Voir le panier** `/cart/`

## 🔑 Différences clés

### Utilisateur **connecté** :
- Panier sauvegardé en DB (modèles Cart/CartItem)
- **Stock décrémenté** automatiquement
- Panier persistant

### Utilisateur **non connecté** :
- Panier en session
- Stock **non modifié**
- Panier temporaire

## 📁 Structure (Clean Architecture)

```
cart/
├── models.py          # Modèles Cart et CartItem (données)
├── cart_service.py    # ⭐ CartService : toute la logique métier
└── views.py           # Vues ultra-simples (3 lignes!)
shop/
├── models.py          # Modèle Product
└── views.py           # Vue index
templates/             # Templates avec Simple.css
```

## ✨ Architecture Service Layer

### `CartService` - Le cerveau du panier

```python
cart_service = CartService(request)
cart_service.add_item(product, quantity)  # Gère auto session vs DB
items = cart_service.get_items()          # Format uniforme
total = cart_service.get_total()          # Calcul automatique
cart_service.clear()                      # Vider le panier
```

**Avantages :**
- 🎯 Séparation des responsabilités
- 🧪 Facilement testable
- 📝 Code lisible et maintenable
- ♻️ Réutilisable (API, CLI, etc.)
- 🔒 La vue ne sait pas si l'utilisateur est connecté !

## 🎓 Concepts démontrés

- **Service Layer Pattern**
- **Encapsulation** de la logique métier
- **Abstraction** (session vs DB transparent)
- **Single Responsibility Principle**
- **DRY** (Don't Repeat Yourself)
