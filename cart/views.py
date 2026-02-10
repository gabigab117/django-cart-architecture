from django.shortcuts import render, redirect, get_object_or_404
from shop.models import Product
from cart.cart_service import CartService

# Create your views here.

def add_to_cart(request, product_id):
    """Ajoute un produit au panier - Version CLEAN avec service"""
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))
    
    # Le service gère tout : session vs DB, stock, messages, etc.
    cart_service = CartService(request)
    success = cart_service.add_item(product, quantity)
    
    if success:
        return redirect('cart_detail')
    else:
        return redirect('index')


def cart_detail(request):
    """Affiche le panier - Version CLEAN avec service"""
    cart_service = CartService(request)
    
    return render(request, 'shop/cart.html', {
        'cart_items': cart_service.get_items(),
        'total': cart_service.get_total(),
        'is_authenticated': request.user.is_authenticated
    })
