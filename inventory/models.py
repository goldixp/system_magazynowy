from django.db import models

class Product(models.Model):
    """
    Model produktu w magazynie.
    """
    CATEGORY_CHOICES = [
        ('Telefon', 'Telefon'),
        ('Laptop', 'Laptop'),
        ('Monitor', 'Monitor'),
        ('Akcesoria', 'Akcesoria'),
        ('Drukarka', 'Drukarka'),
        ('Inne', 'Inne'),
    ]

    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='Inne')
    name = models.CharField(max_length=255, verbose_name="Nazwa produktu")
    sku = models.CharField(max_length=50, unique=True) 
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='Inne')
    description = models.TextField(blank=True, null=True, verbose_name="Opis produktu")
    current_stock = models.IntegerField(default=0, verbose_name="Aktualny stan magazynowy")
    
    def __str__(self):
        return f"{self.name} ({self.sku})"
    
    def save(self, *args, **kwargs):
        if not self.sku:
            prefix = self.category[:3].upper()
            
            last_product = Product.objects.filter(category=self.category).order_by('id').last()
            
            if last_product and '-' in last_product.sku:
               
                last_number = int(last_product.sku.split('-')[1])
                new_number = last_number + 1
            else:
                new_number = 1
                
            self.sku = f"{prefix}-{new_number:04d}"
            
        super().save(*args, **kwargs)
        
            


class StockMovement(models.Model):
    """
    Model historii operacji
    """
    MOVEMENT_CHOICES = [
        ('IN', 'Dostawa'),
        ('OUT', 'Wydanie'),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='movements', verbose_name="Produkt")
    movement_type = models.CharField(max_length=3, choices=MOVEMENT_CHOICES, verbose_name="Typ operacji")
    quantity = models.PositiveIntegerField(verbose_name="Ilość sztuk")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Data i godzina operacji")

    def __str__(self):
        return f"{self.get_movement_type_display()} - {self.product.name} ({self.quantity} szt.)"