from django.contrib import admin
from django.urls import path
from inventory.views import add_product,product_list, stock_movement_list, add_stock_movement

urlpatterns = [
    path('', product_list, name='home'),
    path('admin/', admin.site.urls),
    path('products/', product_list, name='product_list'),
    path('movements/', stock_movement_list, name='stock_movement_list'),
    path('movements/add/', add_stock_movement, name='add_stock_movement'),
    path('products/add/', add_product, name='add_product_form')
]