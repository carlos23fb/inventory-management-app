from django import forms
from .models import Product, Category, Unit


class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ('product_name', 'unit', 'category',
                  'quantity', 'description',)


class CategoryForm(forms.ModelForm):

    class Meta:
        model = Category
        fields = ('name',)


class UnitForm(forms.ModelForm):

    class Meta:
        model = Unit
        fields = ("unit",)
