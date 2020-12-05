from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('home/customer', views.home_customer, name='home_customer'),
    path('dashboard/admin', views.dashboard_admin, name='dashboard_admin'),
    path('products_list', views.products_list, name='products'),
    path('product/new', views.product_new, name='product_new'),
    path('category/new', views.new_category, name="new_category"),
    path('unit/new', views.new_unit, name='new_unit'),
    path('orders/new', views.new_order, name='new_order'),
    path('orders', views.orders_list, name="orders_list"),
    path('customer/orders', views.customer_orders, name="customer_orders"),
    path('<int:order_id>', views.order, name="order"),
    path("<int:order_id>/add", views.add, name="add"),
    path("<int:order_id>/deliver", views.deliver, name="deliver"),
    path("<int:order_id>/reject", views.reject, name="reject"),
    path('<int:order_id>/add_item', views.add_item, name="add_item"),
    path("add/item", views.item_order, name="item_order"),
    path("<int:order_id>/remove", views.remove_item, name="remove_item"),
    path("stock", views.stock, name="stock"),
    path("add/stock", views.add_stock, name="add_stock"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("customer/stock", views.customer_stock, name="customer_stock")
]
