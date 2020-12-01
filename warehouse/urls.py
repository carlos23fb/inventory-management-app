from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('products_list', views.products_list, name='products'),
    path('product/new', views.product_new, name='product_new'),
    path('category/new', views.new_category, name="new_category"),
    path('unit/new', views.new_unit, name='new_unit'),
    path('orders/new', views.new_order, name='new_order'),
    path('orders', views.orders_list, name="orders_list"),
    path('<int:order_id>', views.order, name="order"),
    path("<int:order_id>/add", views.add, name="add"),
    path('<int:order_id>/add_item', views.add_item, name="add_item"),
    path("add/item", views.item_order, name="item_order"),
    path("stock", views.stock, name="stock"),
    path("add/stock", views.add_stock, name="add_stock")

]
