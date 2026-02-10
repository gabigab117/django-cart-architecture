from django.contrib import messages
from cart.models import Cart, CartItem


class CartService:
    """Service complet pour gérer le panier (session ou DB selon l'authentification)"""
    
    def __init__(self, request):
        self.request = request
        self.user = request.user
        self.is_authenticated = request.user.is_authenticated
    
    def add_item(self, product, quantity=1):
        """Ajoute un produit au panier (gère auto session vs DB)"""
        if self.is_authenticated:
            return self._add_to_db_cart(product, quantity)
        else:
            return self._add_to_session_cart(product, quantity)
    
    def _add_to_db_cart(self, product, quantity):
        """Ajoute au panier en base de données"""
        cart, _ = Cart.objects.get_or_create(user=self.user)
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product
        )
        
        if not created:
            cart_item.quantity += quantity
        else:
            cart_item.quantity = quantity
        cart_item.save()
        
        # Gestion du stock
        if product.stock >= quantity:
            product.stock -= quantity
            product.save()
            messages.success(self.request, f'{product.name} ajouté au panier')
            return True
        else:
            messages.error(self.request, f'Stock insuffisant pour {product.name}')
            return False
    
    def _add_to_session_cart(self, product, quantity):
        """Ajoute au panier en session"""
        cart = self.request.session.get('cart', {})
        product_key = str(product.id)
        
        if product_key in cart:
            cart[product_key]['quantity'] += quantity
        else:
            cart[product_key] = {
                'name': product.name,
                'price': float(product.price),
                'quantity': quantity
            }
        
        self.request.session['cart'] = cart
        self.request.session.modified = True
        messages.success(self.request, f'{product.name} ajouté au panier')
        return True
    
    def get_items(self):
        """Récupère les items du panier (format uniforme)"""
        if self.is_authenticated:
            return self._get_db_items()
        else:
            return self._get_session_items()
    
    def _get_db_items(self):
        """Items depuis la base de données"""
        cart = Cart.objects.filter(user=self.user).first()
        return cart.items.all() if cart else []
    
    def _get_session_items(self):
        """Items depuis la session (formatés comme des objets)"""
        cart = self.request.session.get('cart', {})
        items = []
        
        for _, item_data in cart.items():
            items.append({
                'product_name': item_data['name'],
                'quantity': item_data['quantity'],
                'price': item_data['price'],
                'total': item_data['price'] * item_data['quantity']
            })
        
        return items
    
    def get_total(self):
        """Calcule le total du panier"""
        items = self.get_items()
        
        if self.is_authenticated:
            return sum(item.get_total_price() for item in items)
        else:
            return sum(item['total'] for item in items)
    
    def clear(self):
        """Vide le panier"""
        if self.is_authenticated:
            cart = Cart.objects.filter(user=self.user).first()
            if cart:
                cart.items.all().delete()
        else:
            self.request.session['cart'] = {}
            self.request.session.modified = True


"""
request.session = {
    'cart': {
        '1': {
            'name': 'MacBook Pro',
            'price': 2499.99,
            'quantity': 2
        },
        '3': {
            'name': 'iPhone 15',
            'price': 999.0,
            'quantity': 1
        },
        '7': {
            'name': 'AirPods Pro',
            'price': 249.0,
            'quantity': 3
        }
    },
    # ... autres données de session potentielles
}
"""