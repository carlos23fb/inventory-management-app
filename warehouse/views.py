from .forms import ProductForm, CategoryForm, UnitForm, OrderForm, ItemForm, WarehouseStockForm
from django.shortcuts import redirect, render
from .models import GeneralOrder, Product, ItemQuantity, WarehouseStock, Customer, WareHouse
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required


# Create your views here.

@login_required(login_url="login")
def home(request):
    return render(request, 'warehouse/home.html')


@login_required(login_url="login")
def products_list(request):
    products = Product.objects.all().order_by("-created_date")
    return render(request, 'warehouse/products_list.html', {
        'products': products

    })


@login_required(login_url="login")
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


@login_required(login_url="login")
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


@login_required(login_url="login")
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


@login_required(login_url="login")
def orders_list(request):
    orders = GeneralOrder.objects.all()
    return render(request, 'warehouse/orders_list.html', {
        'orders': orders
    })


@login_required(login_url="login")
def order(request, order_id):
    form = ItemForm()
    warehouse_name = Customer.objects.get(user=request.user.id)
    id_warehouse = warehouse_name.user_warehouse.id
    stock = WarehouseStock.objects.filter(warehouse_id=id_warehouse)
    print(id_warehouse)
    items = ItemQuantity.objects.filter(order_id=order_id)
    order = GeneralOrder.objects.get(pk=order_id)
    return render(request, "warehouse/order.html", {
        "stock": stock,
        "form": form,
        "items": items,
        "order": order
    })


@login_required(login_url="login")
def add(request, order_id):
    if request.method == "POST":
        order = GeneralOrder.objects.get(pk=order_id)
        product = Product.objects.get(pk=int(request.POST["product"]))
        product.order.add(order)
        return HttpResponseRedirect(reverse('order', args=(order_id,)))


@login_required(login_url="login")
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


@login_required(login_url="login")
def add_item(request, order_id):
    if request.method == "POST":
        form = ItemForm(request.POST)
        if form.is_valid():
            product = Product.objects.get(pk=request.POST["product_pk"])
            print(request.POST["product_pk"])
            product_quantity = product.quantity
            update_value = product_quantity - form.cleaned_data["item_quantity"]
            form.cleaned_data["item_quantity"]
            Product.objects.filter(pk=request.POST["product_pk"]).update(
                quantity=update_value)

            warehouse_name = Customer.objects.get(user=request.user.id)
            id_warehouse = warehouse_name.user_warehouse.id
            warehouse_item = WarehouseStock.objects.get(
                product_id=request.POST["product_pk"], warehouse_id=id_warehouse)
            item_quantity = warehouse_item.stock
            item_update = item_quantity - form.cleaned_data["item_quantity"]
            WarehouseStock.objects.filter(
                product_id=request.POST["product_pk"], warehouse_id=id_warehouse).update(stock=item_update)

        item = ItemQuantity(
            item_quantity=form.cleaned_data["item_quantity"], order=GeneralOrder.objects.get(pk=order_id), product=Product.objects.get(pk=request.POST["product_pk"]))

        item.save()
        return HttpResponseRedirect(reverse('order', args=(order_id,)))


@login_required(login_url="login")
def remove_item(request, order_id):
    if request.method == "POST":
        product = Product.objects.get(pk=request.POST["product_id"])
        product_quantity = product.quantity
        update_value = product_quantity + int(request.POST["item_quantity"])
        Product.objects.filter(pk=request.POST["product_id"]).update(
            quantity=update_value)

        warehouse_name = Customer.objects.get(user=request.user.id)
        id_warehouse = warehouse_name.user_warehouse.id
        warehouse_item = WarehouseStock.objects.get(
            product_id=request.POST["product_id"], warehouse_id=id_warehouse)
        item_quantity = warehouse_item.stock
        item_update = item_quantity + int(request.POST["item_quantity"])
        WarehouseStock.objects.filter(
            product_id=request.POST["product_id"], warehouse_id=id_warehouse).update(stock=item_update)
        ItemQuantity.objects.filter(pk=request.POST["item_id"]).delete()
        return HttpResponseRedirect(reverse('order', args=(order_id,)))


@login_required(login_url="login")
def new_order(request):
    if request.method == "POST":
        warehouse_name = Customer.objects.get(user=request.user.id)
        id_warehouse = warehouse_name.user_warehouse.id
        form = OrderForm(request.POST)
        if form.is_valid():
            order = GeneralOrder(
                order_name=form.cleaned_data["order_name"], warehouse=WareHouse.objects.get(pk=id_warehouse))
            order.save()
            return redirect("orders_list")
    else:
        form = OrderForm()
        return render(request, "warehouse/new_order.html", {
            "form": form
        })


@login_required(login_url="login")
def stock(request):
    form = WarehouseStockForm()
    return render(request, "warehouse/add_stock.html", {
        "form": form
    })


@login_required(login_url="login")
def item_order(request):
    form = ItemForm()
    return render(request, "warehouse/item.html", {
        "form": form
    })


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("home"))
        else:
            return render(request, "warehouse/login.html", {
                "message": "Invalid Credentials"
            })

    return render(request, "warehouse/login.html")


def logout_view(request):
    logout(request)
    return render(request, 'warehouse/login.html', {
        "logout_message": "Logged Out"
    })
