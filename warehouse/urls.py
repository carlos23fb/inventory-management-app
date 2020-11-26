from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('products_list', views.products_list, name='products'),
    path('product/new', views.product_new, name='product_new'),
    path('category/new', views.new_category, name="new_category"),
    path('unit/new', views.new_unit, name='new_unit')
]
