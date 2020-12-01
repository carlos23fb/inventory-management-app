from django import forms
from .models import ItemQuantity, Product, Category, Unit, GeneralOrder, WarehouseStock


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
