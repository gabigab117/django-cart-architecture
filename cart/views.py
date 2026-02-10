from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from shop.models import Product
from cart.models import Cart, CartItem

# Create your views here.

def add_to_cart(request, product_id):
    """Version SALE - tout dans la vue!"""
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))
    
    if request.user.is_authenticated:
        # Logique pour user connecté
        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart, 
            product=product
        )
        if not created:
            cart_item.quantity += quantity
        else:
            cart_item.quantity = quantity
        cart_item.save()
        
        # Décrémentation du stock pour users authentifiés
        if product.stock >= quantity:
            product.stock -= quantity
            product.save()
        else:
            messages.error(request, f'Stock insuffisant pour {product.name}')
            return redirect('index')
    else:
        # Logique pour session
        cart = request.session.get('cart', {})
        product_key = str(product_id)
        if product_key in cart:
            cart[product_key]['quantity'] += quantity
        else:
            cart[product_key] = {
                'name': product.name,
                'price': float(product.price),
                'quantity': quantity
            }
        request.session['cart'] = cart
        request.session.modified = True
    
    messages.success(request, f'{product.name} ajouté au panier')
    return redirect('cart_detail')


def cart_detail(request):
    """Affiche le panier"""
    if request.user.is_authenticated:
        # Panier DB
        cart = Cart.objects.filter(user=request.user).first()
        cart_items = cart.items.all() if cart else []
        total = sum(item.get_total_price() for item in cart_items)
    else:
        # Panier session
        cart = request.session.get('cart', {})
        cart_items = []
        total = 0
        for product_id, item_data in cart.items():
            cart_items.append({
                'product_name': item_data['name'],
                'quantity': item_data['quantity'],
                'price': item_data['price'],
                'total': item_data['price'] * item_data['quantity']
            })
            total += item_data['price'] * item_data['quantity']
    
    return render(request, 'shop/cart.html', {
        'cart_items': cart_items,
        'total': total,
        'is_authenticated': request.user.is_authenticated
    })
