from django.contrib import admin
from.models import Category, Product, Unit, WareHouse, GeneralOrder, ItemQuantity
# Register your models here.


admin.site.register(Category)
admin.site.register(Unit)
admin.site.register(Product)
admin.site.register(WareHouse)
admin.site.register(GeneralOrder)
admin.site.register(ItemQuantity)
