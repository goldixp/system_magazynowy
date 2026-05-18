from django.shortcuts import render
from .models import Product, StockMovement

def product_list(request):
    products = Product.objects.all()
    return render(request, 'inventory/product_list.html', {'products': products})

def stock_movement_list(request):
    movements = StockMovement.objects.all()
    return render(request, 'inventory/stock_movement_list.html', {'movements': movements})