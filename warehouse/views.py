from .forms import ProductForm, CategoryForm, UnitForm, OrderForm, ItemForm, WarehouseStockForm
from django.shortcuts import redirect, render
from .models import GeneralOrder, Product, ItemQuantity, WarehouseStock
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
    form = ItemForm()
    items = ItemQuantity.objects.filter(order_id=order_id)
    order = GeneralOrder.objects.get(pk=order_id)
    all_products = Product.objects.all().order_by("-created_date")
    return render(request, "warehouse/order.html", {
        "form": form,
        "items": items,
        "order": order,
        "all_products": all_products,
        "products": order.orders.all(),
        "non_products": Product.objects.exclude(order=order).all()
    })


def add(request, order_id):
    if request.method == "POST":
        order = GeneralOrder.objects.get(pk=order_id)
        product = Product.objects.get(pk=int(request.POST["product"]))
        product.order.add(order)
        return HttpResponseRedirect(reverse('order', args=(order_id,)))


def add_item(request, order_id):
    if request.method == "POST":
        form = ItemForm(request.POST)
        print(request.POST["item_quantity"])
        if form.is_valid():
            item = ItemQuantity(
                item_quantity=form.cleaned_data["item_quantity"], order=GeneralOrder.objects.get(pk=order_id), product=Product.objects.get(pk=request.POST["product_id"]))
            item.save()
            return HttpResponseRedirect(reverse('order', args=(order_id,)))


def add_stock(request):
    if request.method == "POST":
        stock = int(request.POST["stock"])
        product = Product.objects.get(pk=request.POST["product_id"])
        product_quantity = product.quantity
        update_value = stock + product_quantity
        print(update_value)
        Product.objects.filter(pk=request.POST["product_id"]).update(
            quantity=update_value)

        if WarehouseStock.objects.filter(product_id=request.POST["product_id"], warehouse_id=request.POST["warehouse_id"]).exists():
            warehouse_item = WarehouseStock.objects.get(
                product_id=request.POST["product_id"])
            item_quantity = warehouse_item.stock
            item_update = stock + item_quantity
            WarehouseStock.objects.filter(
                product_id=request.POST["product_id"]).update(stock=item_update)
        else:
            form = WarehouseStockForm(request.POST)
            form.save()
        return HttpResponseRedirect(reverse("add_stock"))

    else:
        return redirect("stock")


def stock(request):
    form = WarehouseStockForm()
    return render(request, "warehouse/add_stock.html", {
        "form": form
    })


def new_order(request):
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.save()
            return redirect("orders_list")
    else:
        form = OrderForm()
        return render(request, "warehouse/new_order.html", {
            "form": form
        })


def item_order(request):
    form = ItemForm()
    return render(request, "warehouse/item.html", {
        "form": form
    })
