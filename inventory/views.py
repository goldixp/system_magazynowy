from django.shortcuts import render, redirect
from django.db import transaction
from .models import Product, StockMovement
from .forms import StockMovementForm, ProductForm
from django.shortcuts import render, redirect, get_object_or_404

def product_list(request):
    query = request.GET.get('q')
    if query:
        products = Product.objects.filter(name__icontains=query)
    else:
        products = Product.objects.all()
    
    return render(request, 'inventory/product_list.html', {'products': products, 'query': query})

def stock_movement_list(request):
    movements = StockMovement.objects.all().order_by('-created_at')
    
    start_date = request.GET.get('start_date', '')
    end_date = request.GET.get('end_date', '')
    error_message = None  

   
    if start_date and end_date and start_date > end_date:
        error_message = "Błąd: Data końcowa nie może być wcześniejsza niż data początkowa!"
    else:
  
        if start_date:
            movements = movements.filter(created_at__gte=start_date)
        if end_date:
            movements = movements.filter(created_at__lte=f"{end_date} 23:59:59")
    
    context = {
        'movements': movements,
        'start_date': start_date, 
        'end_date': end_date,
        'error_message': error_message 
    }
    return render(request, 'inventory/stock_movement_list.html', context)
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

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product_url = request.build_absolute_uri()
    
    # Wyciągamy historię ruchów TYLKO dla tego produktu
    movements = StockMovement.objects.filter(product=product).order_by('-created_at')

    # Obsługa formularza na tej samej stronie
    if request.method == 'POST':
        form = StockMovementForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                movement = form.save(commit=False)
                # Nadpisujemy produkt z formularza tym, na którego stronie jesteśmy
                movement.product = product
                
                # Zabezpieczamy produkt do edycji
                locked_product = Product.objects.select_for_update().get(id=product.id)
                
                if movement.movement_type == 'IN':
                    locked_product.current_stock += movement.quantity
                elif movement.movement_type == 'OUT':
                    locked_product.current_stock -= movement.quantity
                
                locked_product.save()
                movement.save()
                
            # Po zapisaniu odświeżamy stronę szczegółów produktu
            return redirect('product_detail', pk=product.pk)
    else:
        # Inicjujemy pusty formularz, ustawiając domyślny produkt
        form = StockMovementForm(initial={'product': product})

    context = {
        'product': product, 
        'product_url': product_url,
        'movements': movements,
        'form': form
    }
    
    return render(request, 'inventory/product_detail.html', context)

def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)
        
    return render(request, 'inventory/product_add_form.html', {'form': form})

def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    
    if request.method == 'POST':
        product.delete()
        return redirect('product_list')
        
    return render(request, 'inventory/product_confirm_delete.html', {'product': product})