from django.shortcuts import render
from shop.models import Product

# Create your views here.

def index(request):
    """Affiche tous les produits"""
    products = Product.objects.all()
    return render(request, 'shop/index.html', {'products': products})
