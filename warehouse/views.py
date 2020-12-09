from .forms import ProductForm, CategoryForm, UnitForm, OrderForm, ItemForm, WarehouseStockForm
from django.shortcuts import redirect, render
from .models import GeneralOrder, Product, ItemQuantity, WarehouseStock, Customer, WareHouse
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated, allowed_users
import pandas as pd

# Create your views here.

@login_required(login_url="login")
def home(request):
    group = request.user.groups.all()[0].name
    if group == "customer":
        return redirect('home_customer')
    else:
        return redirect("dashboard_admin")


def home_customer(request):
    warehouse_name = Customer.objects.get(user=request.user.id)
    id_warehouse = warehouse_name.user_warehouse.id
    orders = GeneralOrder.objects.filter(
        status="Pending", warehouse=id_warehouse)
    pending_orders = GeneralOrder.objects.filter(
        status="Pending", warehouse=id_warehouse).count()
    delivered = GeneralOrder.objects.filter(
        status="Delivered", warehouse=id_warehouse).count()
    rejected = GeneralOrder.objects.filter(
        status="Rejected", warehouse=id_warehouse).count()
    return render(request, 'warehouse/home_customer.html', {
        'orders': orders,
        'pending': pending_orders,
        'delivered': delivered,
        'rejected': rejected
    })


@login_required(login_url="login")
@allowed_users(allowed_roles=['admin'])
def dashboard_admin(request):
    items_table = ItemQuantity.objects.all().values()
    producs_table = Product.objects.all().values()
    orders_table = GeneralOrder.objects.all().values()
    df1 = pd.DataFrame.from_dict(items_table)
    df2 = pd.DataFrame.from_dict(producs_table)
    df3 = pd.DataFrame.from_dict(orders_table)

    df4 = pd.merge(df1,df3, how='inner', left_on='order_id', right_on='id')
    df5 = pd.merge(df4,df2, how='inner', left_on='product_id', right_on='id')
    orders = GeneralOrder.objects.filter(
        status="Pending").order_by("date_created")
    pending_orders = GeneralOrder.objects.filter(
        status="Pending").count()
    delivered = GeneralOrder.objects.filter(
        status="Delivered").count()
    rejected = GeneralOrder.objects.filter(
        status="Rejected").count()
    return render(request, 'warehouse/admin_dashboard.html', {
        'orders': orders,
        "pending": pending_orders,
        "rejected": rejected,
        "delivered": delivered,
        'data': df5.to_html
    })


@login_required(login_url="login")
def products_list(request):
    products = Product.objects.all().order_by("-created_date")
    return render(request, 'warehouse/products_list.html', {
        'products': products
    })


@login_required(login_url="login")
@allowed_users(allowed_roles=['admin'])
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
@allowed_users(allowed_roles=['admin'])
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
@allowed_users(allowed_roles=['admin'])
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
@allowed_users(allowed_roles=['admin'])
def orders_list(request):
    orders = GeneralOrder.objects.filter(status="Pending")
    return render(request, 'warehouse/orders_list.html', {
        'orders': orders
    })


@login_required(login_url="login")
def customer_orders(request):
    warehouse_name = Customer.objects.get(user=request.user.id)
    id_warehouse = warehouse_name.user_warehouse.id
    orders = GeneralOrder.objects.filter(
        status="Pending", warehouse=id_warehouse)
    pending_orders = GeneralOrder.objects.filter(
        status="Pending", warehouse=id_warehouse).count()
    delivered = GeneralOrder.objects.filter(
        status="Delivered", warehouse=id_warehouse).count()
    rejected = GeneralOrder.objects.filter(
        status="Rejected", warehouse=id_warehouse).count()
    return render(request, 'warehouse/orders_list.html', {
        'orders': orders,
        'pending': pending_orders,
        'delivered': delivered,
        'rejected': rejected
    })


@login_required(login_url="login")
def order(request, order_id):
    group = request.user.groups.all()[0].name
    order = GeneralOrder.objects.get(pk=order_id)

    if group == "customer" and (order.status == "Rejected" or order.status == "Rejected"):
        return render(request, 'warehouse/not_allow.html')
    else:
        item_number = ItemQuantity.objects.filter(order_id=order_id).count()
        form = ItemForm()
        warehouse_name = Customer.objects.get(user=request.user.id)
        id_warehouse = warehouse_name.user_warehouse.id
        stock = WarehouseStock.objects.filter(warehouse_id=id_warehouse)
        items = ItemQuantity.objects.filter(order_id=order_id)
        return render(request, "warehouse/order.html", {
            "stock": stock,
            "form": form,
            "items": items,
            "order": order,
            "item_number": item_number,
            'group': group
        })


@login_required(login_url="login")
def customer_stock(request):
    warehouse_name = Customer.objects.get(user=request.user.id)
    id_warehouse = warehouse_name.user_warehouse.id
    stock = WarehouseStock.objects.filter(warehouse_id=id_warehouse)

    return render(request, "warehouse/customer_stock.html", {
        "stock": stock
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
        Product.objects.filter(pk=request.POST["product_id"]).update(
            quantity=update_value)

        if WarehouseStock.objects.filter(product_id=request.POST["product_id"], warehouse_id=request.POST["warehouse_id"]).exists():
            warehouse_item = WarehouseStock.objects.get(
                product_id=request.POST["product_id"], warehouse_id=request.POST["warehouse_id"])
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
            product_quantity = product.quantity
            update_value = product_quantity - \
                form.cleaned_data["item_quantity"]
            form.cleaned_data["item_quantity"]
            if update_value >= 0:
                Product.objects.filter(pk=request.POST["product_pk"]).update(
                    quantity=update_value)

                warehouse_name = Customer.objects.get(user=request.user.id)
                id_warehouse = warehouse_name.user_warehouse.id
                warehouse_item = WarehouseStock.objects.get(
                    product_id=request.POST["product_pk"], warehouse_id=id_warehouse)
                item_quantity = warehouse_item.stock
                item_update = item_quantity - \
                    form.cleaned_data["item_quantity"]
                WarehouseStock.objects.filter(
                    product_id=request.POST["product_pk"], warehouse_id=id_warehouse).update(stock=item_update)

                item = ItemQuantity(
                    item_quantity=form.cleaned_data["item_quantity"], order=GeneralOrder.objects.get(pk=order_id), product=Product.objects.get(pk=request.POST["product_pk"]))

                item.save()
                return HttpResponseRedirect(reverse('order', args=(order_id,)))
            else:
                return HttpResponseRedirect(reverse('order', args=(order_id,)))


@login_required(login_url="login")
@allowed_users(allowed_roles=['admin'])
def deliver(request, order_id):
    GeneralOrder.objects.filter(pk=order_id).update(status="Delivered")
    return redirect('orders_list')


@login_required(login_url="login")
@allowed_users(allowed_roles=['admin'])
def reject(request, order_id):
    GeneralOrder.objects.filter(pk=order_id).update(status="Rejected")
    return redirect('orders_list')


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
            return redirect("customer_orders")
    else:
        form = OrderForm()
        return render(request, "warehouse/new_order.html", {
            "form": form
        })


@login_required(login_url="login")
@allowed_users(allowed_roles=['admin'])
def stock(request):
    form = WarehouseStockForm()
    return render(request, "warehouse/add_stock.html", {
        "form": form
    })


@login_required(login_url="login")
@allowed_users(allowed_roles=['admin'])
def item_order(request):
    form = ItemForm()
    return render(request, "warehouse/item.html", {
        "form": form
    })


@unauthenticated
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
