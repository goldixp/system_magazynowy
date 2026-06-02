from django.shortcuts import render, redirect
from django.db import transaction
from .models import Product, StockMovement
from .forms import StockMovementForm, ProductForm

def product_list(request):
    query = request.GET.get('q')
    if query:
        products = Product.objects.filter(name__icontains=query)
    else:
        products = Product.objects.all()
    
    return render(request, 'inventory/product_list.html', {'products': products, 'query': query})

def stock_movement_list(request):
    movements = StockMovement.objects.all().order_by('-created_at')
    return render(request, 'inventory/stock_movement_list.html', {'movements': movements})

def add_stock_movement(request):
    if request.method == 'POST':
        form = StockMovementForm(request.POST)
        
        if form.is_valid():
            with transaction.atomic():
                movement = form.save(commit=False)
                product = Product.objects.select_for_update().get(id=movement.product.id)
                
                if movement.movement_type == 'IN':
                    product.current_stock += movement.quantity
                elif movement.movement_type == 'OUT':
                    product.current_stock -= movement.quantity
                
                product.save()
                movement.save()
                
            return redirect('stock_movement_list')
    else:
        form = StockMovementForm()
        
    return render(request, 'inventory/stock_movement_form.html', {'form': form})

def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save() 
            return redirect('product_list') 
    else:
        form = ProductForm()
        
    return render(request, 'inventory/product_add_form.html', {'form': form})
        