from django.contrib import admin
from.models import Categorie, Product, Unit, WareHouse, GeneralOrder, ItemQuantity, Customer, Suplier, WarehouseStock
# Register your models here.


admin.site.register(Categorie)
admin.site.register(Unit)
admin.site.register(Product)
admin.site.register(WareHouse)
admin.site.register(GeneralOrder)
admin.site.register(ItemQuantity)
admin.site.register(Customer)
admin.site.register(Suplier)
admin.site.register(WarehouseStock)
