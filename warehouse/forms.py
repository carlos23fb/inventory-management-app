from django import forms
from .models import ItemQuantity, Product, Categorie, Unit, GeneralOrder, WarehouseStock


class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ('product_name', 'unit', 'categorie',
                  'quantity', 'description',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['product_name'].widget.attrs.update(
            {'class': 'form-control col-5'})
        self.fields['unit'].widget.attrs.update(
            {'class': 'form-control col-3'})
        self.fields['categorie'].widget.attrs.update(
            {'class': 'form-control col-3'})
        self.fields['quantity'].widget.attrs.update(
            {'class': 'form-control col-6'})
        self.fields['description'].widget.attrs.update(
            {'class': 'form-control col-12', 'placeholder': "Product description"})


class CategoryForm(forms.ModelForm):

    class Meta:
        model = Categorie
        fields = ('name',)


class UnitForm(forms.ModelForm):

    class Meta:
        model = Unit
        fields = ("unit",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['unit'].widget.attrs.update(
            {'class': 'form-control col-3'})


class OrderForm(forms.ModelForm):
    class Meta:
        model = GeneralOrder
        fields = ('order_name', 'warehouse')


class ItemForm(forms.ModelForm):

    class Meta:
        model = ItemQuantity
        fields = ("item_quantity", "order", "product")


class WarehouseStockForm(forms.ModelForm):

    class Meta:
        model = WarehouseStock
        fields = ('warehouse_id', 'product_id', 'stock')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['warehouse_id'].widget.attrs.update(
            {'class': 'form-control col-6'})
        self.fields['product_id'].widget.attrs.update(
            {'class': 'form-control col-6'})
        self.fields['stock'].widget.attrs.update(
            {'class': 'form-control col-12'})
