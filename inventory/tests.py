from django.test import TestCase
from django.contrib.auth.models import User
from .models import Product, StockMovement
from .forms import StockMovementForm 

class InventoryTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        
        self.product = Product.objects.create(
            name='Produkt do testow',
            sku='TEST-001',
            description='Opis produktu do testow',
            current_stock=10  
        )

    def test_invalid_stock_movement(self):
        
        form_data = {
            'product': self.product.id,
            'movement_type': 'OUT',
            'quantity': 15  
        }
        
        form = StockMovementForm(data=form_data)
        
        self.assertFalse(form.is_valid())
        
        self.assertIn('Niewystarczająca ilość towaru', str(form.errors))

    def test_valid_stock_movement(self):
        form_data = {
            'product': self.product.id,
            'movement_type': 'OUT',
            'quantity': 5  
        }
        
        form = StockMovementForm(data=form_data)
        self.assertTrue(form.is_valid())