import datetime
import pytz

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .form import *
from .models import *
from .rate import rate



@login_required
def general(request):

    shop = Shop.objects.all()
    status = Status.objects.all()
    category = Category.objects.all()
    all_client = Client.objects.all()
    try:
        rate_now = Rate.objects.latest('id')
    except Rate.DoesNotExist:
        rate_now = None

    formfilter = FilterForms()

    filter = {}

    shop_filter = request.GET.get('shop')
    status_filter = request.GET.get('stat')
    category_filter = request.GET.get('cat')
    client_filter = request.GET.get('client')

    if request.GET.get('rate'):
        rate()

    if shop_filter or status_filter or category_filter or client_filter:
        if shop_filter:
            shop_filter = get_object_or_404(Shop, title=shop_filter)
            filter['shop'] = shop_filter
        if status_filter:
            status_filter = get_object_or_404(Status, title=status_filter)
            filter['status'] = status_filter
        if category_filter:
            category_filter = get_object_or_404(Category, title=category_filter)
            filter['category'] = category_filter
        if client_filter:
            client_filter = get_object_or_404(Client, pk=client_filter)
            filter['client'] = client_filter

        items = Product.objects.filter(**filter)
    else:
        items = Product.objects.all()

    total_profit = 0
    total_items = 0
    residue_total = 0
    total_clients = len(all_client)

    for i in items:
        total_profit += i.selling_price - i.purchase_price
        residue_total += i.residue
        total_items += 1

    time = {
        'Нью-Йорк': datetime.datetime.now(pytz.timezone("America/New_York")).time(),
        'Италия': datetime.datetime.now(pytz.timezone("Europe/Rome")).time(),
        'Москва': datetime.datetime.now(pytz.timezone("Europe/Moscow")).time(),
    }

    context = {'title': 'Base', 'items': items, 'total': total_profit, 'shop': shop, 'stat': status, 'cat': category,
               'n': total_items, 'formfilter': formfilter, 'client': all_client, 'residue_total': residue_total,
               'clients': total_clients, 'time': time, 'rate': rate_now,
               }

    return render(request, 'base/general.html', context)


@login_required
def new_product(request):
    all_client = Client.objects.all()
    rate_now = Rate.objects.latest('id')

    if request.method == 'POST':
        if 'description' in request.POST.keys():
            form = NewProductForms(request.POST, request.FILES)
            form_client = NewClientForms()
            form_shop = NewShopForms()
            if form.is_valid():
                form.save()
                return redirect('general')
        if 'name' in request.POST.keys():
            form_client = NewClientForms(request.POST)
            form = NewProductForms(request.POST)
            form_shop = NewShopForms()
            if form_client.is_valid():
                form_client.save()
                return redirect('new_product')
        if 'title' in request.POST.keys():
            form_shop = NewShopForms(request.POST)
            form = NewProductForms(request.POST)
            form_client = NewClientForms()
            if form_shop.is_valid():
                form_shop.save()
                return redirect('new_product')
    else:
        form = NewProductForms()
        form_client = NewClientForms()
        form_shop = NewShopForms()

    context = {'title': 'Новый товар', 'form': form, 'client': all_client,
               'form_client': form_client, 'form_shop': form_shop, 'rate': rate_now
               }
    return render(request, 'base/new_product.html', context)


@login_required
def product(request, product_id):
    items = get_object_or_404(Product, pk=product_id)
    profit = items.selling_price - items.purchase_price
    status = Status.objects.all()

    if request.method == 'POST':
        items.status = Status.objects.get(title=request.POST.get('status'))
        items.prepayment = int(request.POST.get('prepayment'))
        items.residue = items.selling_price - items.prepayment
        items.save()
        return redirect('product', product_id=items.pk)

    context = {'title': 'Товар', 'items': items, 'profit': profit, 'status': status}
    return render(request, 'base/product.html', context)


@login_required
def client(request, client_id):
    client = get_object_or_404(Client, pk=client_id)
    product = Product.objects.filter(client=client_id)
    wait1 = 0
    total = 0
    residue_total = 0
    residue_total_del = 0
    all_product = len(product)
    for p in product:
        total += p.selling_price - p.purchase_price
        residue_total += p.residue
        wait = datetime.datetime.now().date() - p.time_create.date()
        if wait.days > wait1:
            wait1 = wait.days
        if p.status.id == 6:
            residue_total_del += p.residue
    context = {'client': client, 'product': product, 'total': total, 'all_product': all_product,
               'residue_total': residue_total, 'wait': wait1, 'residue_total_del': residue_total_del}
    return render(request, 'base/client.html', context)


def start(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('general')
    logout(request)
    return render(request, 'base/start.html')

