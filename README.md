# 🛍️ Shop Example - Version SALE

Projet pour présentation de 30 minutes: Comparaison entre code "sale" (tout dans les vues) et code propre (avec services).

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

## 📁 Structure

- `shop/models.py` - Modèle Product
- `cart/models.py` - Modèles Cart et CartItem
- `shop/views.py` - **VERSION SALE** : toute la logique métier dans les vues!
- `templates/` - Templates avec Simple.css

## ⚡ Prochaine étape

Refactoriser avec un `CartService` pour séparer la logique métier des vues!
# django-cart-architecture
