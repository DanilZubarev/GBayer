import datetime
import pytz

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Sum, Count

from .form import *
from .rate import rate
from .position import *
from dashbord.models import *


@login_required
def general(request):
    if request.user.username in position['CEO']:

        shop = Shop.objects.all()
        status = Status.objects.all()
        category = Category.objects.all()
        all_client = Client.objects.all()
        try:
            rate_now = Rate.objects.latest('id')
        except Rate.DoesNotExist:
            rate_now = None

        formfilter = FilterForms()
        filter = {
            'shop': request.GET.get('shop'),
            'status': request.GET.get('stat'),
            'category': request.GET.get('cat'),
            'client': request.GET.get('client'),
        }

        if request.GET.get('stat_checkbox'):
            stat_checkbox = request.GET.get('stat_checkbox')
            for key in request.GET:
                if key != 'stat_checkbox':
                    item_checkbox = Product.objects.get(pk=key)
                    status_checkbox = Status.objects.get(title=stat_checkbox)
                    item_checkbox.status = status_checkbox
                    item_checkbox.save()

        if request.GET.get('rate'):
            rate()

        if any(filter.values()):
            if filter['shop']:
                filter['shop'] = get_object_or_404(Shop, title=filter['shop'])
            else:
                filter.pop('shop')
            if filter['status']:
                filter['status'] = get_object_or_404(Status, title=filter['status'])
            else:
                filter.pop('status')
            if filter['category']:
                filter['category'] = get_object_or_404(Category, title=filter['category'])
            else:
                filter.pop('category')
            if filter['client']:
                filter['client'] = get_object_or_404(Client, pk=filter['client'])
            else:
                filter.pop('client')

            items = Product.objects.filter(**filter)
        else:
            items = Product.objects.exclude(status=6)

        items_wait = Product.objects.filter(status=1, employee__username__in=position['AM'])

        total_profit = 0
        residue_total = items.aggregate(Sum('residue'))['residue__sum']
        paid_items = items.filter(status=1)
        paid = paid_items.aggregate(Sum('purchase_price'))['purchase_price__sum']
        items_paid = len(paid_items)

        for i in items:
            total_profit += i.selling_price - i.purchase_price

        time = {
            '??????-????????': datetime.datetime.now(pytz.timezone("America/New_York")).time(),
            '????????????': datetime.datetime.now(pytz.timezone("Europe/Rome")).time(),
            '????????????': datetime.datetime.now(pytz.timezone("Europe/Moscow")).time(),
        }

        context = {
            'title': 'Base', 'items': items, 'total': total_profit, 'shop': shop, 'stat': status, 'cat': category,
            'formfilter': formfilter, 'client': all_client, 'residue_total': residue_total,'time': time,
            'rate': rate_now, 'paid': paid, 'items_paid': items_paid,'items_wait': items_wait,
        }

        return render(request, 'base/general.html', context)
    elif request.user.username in position['AM']:
        return redirect('am')
    else:
        return redirect('sk_send')


@login_required
def new_product(request):
    all_client = Client.objects.all()
    rate_now = Rate.objects.latest('id')

    if request.method == 'POST':
        print(request.POST)
        if 'description' in request.POST.keys():
            form = NewProductForms(request.POST, request.FILES)
            form_client = NewClientForms()
            form_shop = NewShopForms()
            form.employee = request.user
            if form.is_valid():
                it = form.save(commit=False)
                it.employee = request.user
                it.profit = it.selling_price - it.purchase_price
                it.have = request.POST.get('have')
                it.save()
                return redirect('general')
        if 'name' in request.POST.keys():
            form_client = NewClientForms(request.POST)
            form = NewProductForms()
            form_shop = NewShopForms()
            if form_client.is_valid():
                form_client.save()
                return redirect('new_product')
        if 'title' in request.POST.keys():
            form_shop = NewShopForms(request.POST)
            form = NewProductForms()
            form_client = NewClientForms()
            if form_shop.is_valid():
                form_shop.save()
                return redirect('new_product')
    else:
        form = NewProductForms()
        form_client = NewClientForms()
        form_shop = NewShopForms()

    context = {'title': '?????????? ??????????', 'form': form, 'client': all_client,
               'form_client': form_client, 'form_shop': form_shop, 'rate': rate_now
               }
    return render(request, 'base/new_product.html', context)


@login_required
def copy_product(request, product_id):
    items = get_object_or_404(Product, pk=product_id)
    all_client = Client.objects.all()
    rate_now = Rate.objects.latest('id')

    if request.method == 'POST':
        if 'name' in request.POST.keys():
            form_client = NewClientForms(request.POST)
            form = NewProductForms(instance=items)
            form_shop = NewShopForms()
            if form_client.is_valid():
                form_client.save()
                return redirect('copy_product', product_id=product_id)
        if 'title' in request.POST.keys():
            form_shop = NewShopForms(request.POST)
            form = NewProductForms(instance=items)
            form_client = NewClientForms()
            if form_shop.is_valid():
                form_shop.save()
                return redirect('copy_product', product_id=product_id)
    else:
        form = NewProductForms(instance=items)
        form_client = NewClientForms()
        form_shop = NewShopForms()

    context = {
        'items': items, 'client': all_client, 'form': form, 'rate': rate_now, 'form_client': form_client,
        'form_shop': form_shop,
    }
    return render(request, 'base/copy_product.html', context)


@login_required
def product(request, product_id):
    items = get_object_or_404(Product, pk=product_id)
    status = Status.objects.all()
    employee = User.objects.all()
    client = Client.objects.all()
    rate_now = Rate.objects.latest('id')
    url = request.META.get("HTTP_REFERER")
    ceo = position['CEO']

    if request.method == 'POST':
        if request.POST.get('client'):
            items.client = Client.objects.get(pk=request.POST.get('client'))
            items.prepayment = int(request.POST.get('selling_price'))
            items.selling_price = int(request.POST.get('selling_price'))
            items.residue = items.selling_price - items.prepayment
            items.profit = items.selling_price - items.purchase_price
            items.have = False
            items.save()
            return redirect('have')
        else:
            items.status = Status.objects.get(title=request.POST.get('status'))
            items.employee = User.objects.get(username=request.POST.get('employee'))
            items.prepayment = int(request.POST.get('prepayment'))
            items.selling_price = int(request.POST.get('selling_price'))
            items.purchase_price = int(request.POST.get('purchase_price'))
            items.residue = items.selling_price - items.prepayment
            items.profit = items.selling_price - items.purchase_price
            items.save()
            if request.path in request.META.get("HTTP_REFERER"):
                url = request.POST.get('url')
            else:
                url = request.META.get("HTTP_REFERER")
            return redirect(url)

    context = {'title': '??????????', 'items': items, 'status': status, 'rate': rate_now,
               'url': url, 'employee': employee, 'ceo': ceo, 'client': client}

    return render(request, 'base/product.html', context)


@login_required
def client(request, client_id):
    if request.user.username not in position['AM']:
        client = get_object_or_404(Client, pk=client_id)
        product = Product.objects.filter(client=client_id)

        if request.method == 'POST':
            if 'name' in request.POST.keys():
                client.telephone = request.POST.get('telephone')
                client.name = request.POST.get('name')
                client.adress = request.POST.get('adress')
                client.save()
                return redirect('client', client_id=client.pk )

        wait1 = 0
        total = product.aggregate(Sum('profit'))['profit__sum']
        residue_total = product.aggregate(Sum('residue'))['residue__sum']
        residue_total_del = 0
        all_product = len(product)
        for p in product:
            wait = datetime.datetime.now().date() - p.time_create.date()
            if wait.days > wait1:
                wait1 = wait.days
            if p.status.title == '???????????????? ?? ????':
                residue_total_del += p.residue
        context = {'client': client, 'product': product, 'total': total, 'all_product': all_product,
                   'residue_total': residue_total, 'wait': wait1, 'residue_total_del': residue_total_del,
                   }
        return render(request, 'base/client.html', context)
    else:
        return redirect('am_client', client_id=client_id)

@login_required
def have(request):
    if request.user.username in position['CEO']:
        have_prod = Product.objects.filter(have=True).order_by('goods__brand')
    else:
        have_prod = Product.objects.filter(have=True).order_by('goods__brand')
        have_prod = have_prod.filter(employee__username=request.user.username)

    ceo = position['CEO']
    sum_purchase_price = have_prod.aggregate(Sum('purchase_price'))['purchase_price__sum']

    context = {'title': '??????????????', 'have': have_prod, 'sum_purchase_price': sum_purchase_price, 'total': len(have_prod),
               'ceo': ceo,
               }
    return render(request, 'base/have.html', context)


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

