from django.db import models
from django.db.models.fields import CharField
from django.db.models.fields.related import ForeignKey

# Create your models here.


class Unit(models.Model):
    unit = models.CharField(max_length=50, null=True, unique=True)

    def __str__(self):

        return f"{self.unit}"


class Category(models.Model):
    name = models.CharField(max_length=50, null=True, unique=True)

    def __str__(self):
        return f"{self.name}"


class WareHouse(models.Model):
    warehouse = models.CharField(max_length=50, null=True, unique=True)

    def __str__(self):
        return f"{self.warehouse}"


class GeneralOrder(models.Model):
    date_created = models.DateField(auto_now=True)
    order_name = CharField(max_length=200, null=True)
    warehouse = models.ForeignKey(WareHouse, on_delete=models.PROTECT)

    def __str__(self):
        return f"Order Id:{self.pk} Warehouse: {self.warehouse} Order Name:{self.order_name}"


class Product(models.Model):
    product_name = models.CharField(max_length=50, null=True, blank=False)
    unit = models.ForeignKey(Unit, on_delete=models.PROTECT)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    created_date = models.DateTimeField(auto_now=True, auto_now_add=False)
    description = models.CharField(max_length=150, blank=True)
    order = models.ManyToManyField(
        GeneralOrder, blank=True, related_name="orders")

    def __str__(self):
        return f"{self.product_name} {self.unit}"


class ItemQuantity(models.Model):
    product = ForeignKey(Product, on_delete=models.PROTECT,
                         null=True, blank=True)
    item_quantity = models.PositiveIntegerField(null=True)
    order = ForeignKey(GeneralOrder, on_delete=models.PROTECT,
                       null=True, blank=True)

    def __str__(self):
        return f"{self.order} Items: {self.item_quantity} {self.product}"
