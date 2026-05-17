from django.db import models

class Product(models.Model):
    """
    Model produktu w magazynie.
    """
    name = models.CharField(max_length=255, verbose_name="Nazwa produktu")
    sku = models.CharField(max_length=100, unique=True, verbose_name="Kod SKU")
    description = models.TextField(blank=True, null=True, verbose_name="Opis produktu")
    current_stock = models.IntegerField(default=0, verbose_name="Aktualny stan magazynowy")

    def __str__(self):
        return f"{self.name} ({self.sku})"


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