from django.contrib.auth.models import User
from django.db import models
from django.db.models.fields import CharField, PositiveIntegerField
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


class WarehouseStock(models.Model):
    warehouse_id = ForeignKey(
        WareHouse, null=True, on_delete=models.PROTECT, related_name="warehouse_id")
    product_id = ForeignKey(
        Product, null=True, on_delete=models.PROTECT, related_name="product_id")
    stock = PositiveIntegerField()


class Customer(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    user_warehouse = models.ForeignKey(
        WareHouse, on_delete=models.PROTECT, null=True)

    def __str__(self):
        return f"User: {self.user} Full Name: {self.full_name} Warehouse: {self.user_warehouse}"


class Suplier(models.Model):
    name = CharField(max_length=200, null=True)
    rfc = CharField(max_length=13, null=True)
    phone = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
