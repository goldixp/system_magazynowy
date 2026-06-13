from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from .models import Product, StockMovement
from .forms import StockMovementForm

# --- testy formularzy ---
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


# --- testy widokow ---
class InventoryViewsTest(TestCase):
    def setUp(self):
        self.product = Product.objects.create(
            name="Testowy Laptop",
            sku="LAP-001",
            current_stock=10
        )
        self.movement = StockMovement.objects.create(
            product=self.product,
            quantity=5,
            movement_type='IN'
        )

    def test_product_detail_404_not_found(self):
        # wywala 404 dla nieistniejacego id
        response = self.client.get(reverse('product_detail', args=[9999]))
        self.assertEqual(response.status_code, 404) 

    def test_product_detail_view_success(self):
        # poprawne ladowanie szczegolow i zewnetrznego api do qr
        response = self.client.get(reverse('product_detail', args=[self.product.id]))
        self.assertEqual(response.status_code, 200) 
        self.assertContains(response, "Testowy Laptop")
        self.assertContains(response, "solsigs") 

    def test_stock_movement_list_date_filter(self):
        # pusta lista (bez filtrowania)
        response = self.client.get(reverse('stock_movement_list'))
        self.assertEqual(response.status_code, 200)
        
        # filtr: dzisiejsza data
        today = timezone.now().strftime('%Y-%m-%d')
        response = self.client.get(reverse('stock_movement_list'), {'start_date': today, 'end_date': today})
        self.assertEqual(response.status_code, 200)

        # zabezpieczenie (walidacja blednych dat od-do)
        response = self.client.get(reverse('stock_movement_list'), {'start_date': '2026-12-31', 'end_date': '2025-01-01'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Błąd")

    def test_product_list_view(self):
        # glowna lista produktow GET
        response = self.client.get(reverse('product_list')) 
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Testowy Laptop")

    def test_product_create_view(self):
        # widok dodawania produktu
        response = self.client.get(reverse('product_create'))
        self.assertEqual(response.status_code, 200)

    def test_product_update_view(self):
        # widok edycji produktu
        response = self.client.get(reverse('product_update', args=[self.product.id]))
        self.assertEqual(response.status_code, 200)

    def test_product_delete_view(self):
        # strona potwierdzenia usuniecia
        response = self.client.get(reverse('product_delete', args=[self.product.id]))
        self.assertEqual(response.status_code, 200)