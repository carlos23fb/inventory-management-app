from django.db import models

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=50, null=True)

    def __str__(self):
        return f"{self.name}"


class WareHouse(models.Model):
    warehouse = models.CharField(max_length=50, null=True)

    def __str__(self):
        return f"{self.warehouse}"


class Unit(models.Model):
    unit = models.CharField(max_length=50, null=True)

    def __str__(self):
        return f"{self.unit}"


class Product(models.Model):
    productName = models.CharField(max_length=50, null=True, blank=False)
    unit = models.ForeignKey(Unit, on_delete=models.PROTECT)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    cuantity = models.PositiveIntegerField()
    created_date = models.DateTimeField(auto_now=False, auto_now_add=False)
    description = models.CharField(max_length=150)

    def __str__(self):
        return f"Product: {self.productName} Cuantity: {self.cuantity} {self.unit} "
