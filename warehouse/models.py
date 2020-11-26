from django.db import models

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=50, null=True, unique=True)

    def __str__(self):
        return f"{self.name}"


class WareHouse(models.Model):
    warehouse = models.CharField(max_length=50, null=True, unique=True)

    def __str__(self):
        return f"{self.warehouse}"


class Unit(models.Model):
    unit = models.CharField(max_length=50, null=True, unique=True)

    def __str__(self):
        return f"{self.unit}"


class Product(models.Model):
    product_name = models.CharField(max_length=50, null=True, blank=False)
    unit = models.ForeignKey(Unit, on_delete=models.PROTECT)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    created_date = models.DateTimeField(auto_now=True, auto_now_add=False)
    description = models.CharField(max_length=150, blank=True)

    def __str__(self):
        return f"Product: {self.product_name} Quantity: {self.quantity} {self.unit} "
