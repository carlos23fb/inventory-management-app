from .forms import ProductForm, CategoryForm, UnitForm
from django.shortcuts import redirect, render
from .models import GeneralOrder, Product, ItemQuantity
from django.http import HttpResponseRedirect
from django.urls import reverse


# Create your views here.


def home(request):
    return render(request, 'warehouse/home.html')


def products_list(request):
    products = Product.objects.all().order_by("-created_date")
    return render(request, 'warehouse/products_list.html', {
        'products': products
    })


def product_new(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.save()
            return redirect('products')
    else:
        form = ProductForm()
        return render(request, 'warehouse/product_edit.html', {
            "form": form
        })


def new_category(request):
    if request.method == "POST":
        form_category = CategoryForm(request.POST)
        if form_category.is_valid():
            form_category.save()
            return redirect("products")
    else:
        form_category = CategoryForm()
        return render(request, 'warehouse/category_edit.html', {
            "form_category": form_category
        })


def new_unit(request):
    if request.method == "POST":
        form_unit = UnitForm(request.POST)
        if form_unit.is_valid():
            form_unit.save()
            return render(request, "warehouse/home.html", {
                "message": "New Unit has ben created succsesfully"
            })
    else:
        form_unit = UnitForm()
        return render(request, 'warehouse/unit_edit.html', {
            "form_unit": form_unit
        })


def orders_list(request):
    orders = GeneralOrder.objects.all()
    return render(request, 'warehouse/orders_list.html', {
        'orders': orders
    })


def order(request, order_id):
    items = ItemQuantity.objects.filter(order_id=order_id)
    order = GeneralOrder.objects.get(pk=order_id)
    return render(request, "warehouse/order.html", {
        "items": items,
        "order": order,
        "products": order.orders.all(),
        "non_products": Product.objects.exclude(order=order).all()
    })


def add(request, order_id):
    if request.method == "POST":
        order = GeneralOrder.objects.get(pk=order_id)
        product = Product.objects.get(pk=int(request.POST["product"]))
        product.order.add(order)
        return HttpResponseRedirect(reverse('order', args=(order_id,)))
