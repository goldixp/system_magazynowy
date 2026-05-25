from django.shortcuts import render, redirect
from django.db import transaction
from .models import Product, StockMovement
from .forms import StockMovementForm

def product_list(request):
    products = Product.objects.all()
    return render(request, 'inventory/product_list.html', {'products': products})

def stock_movement_list(request):
    # NAPRAWIONE: U Ciebie pole to created_at, a nie timestamp!
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