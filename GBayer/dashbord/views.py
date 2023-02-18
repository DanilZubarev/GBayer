import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.db.models import Q, Sum, Count

from base.form import *
from .form import *


@login_required
def am(request):
    shop = Shop.objects.all()
    status = Status.objects.all()
    category = Category.objects.all()
    all_client = Client.objects.all()

    formfilter = FilterForms()
    filter = {
        'shop': request.GET.get('shop'),
        'status': request.GET.get('stat'),
        'category': request.GET.get('cat'),
        'client': request.GET.get('client'),
        'date_from': request.GET.get('from'),
        'date_to': request.GET.get('to'),
    }

    if request.GET.get('stat_checkbox'):
        stat_checkbox = request.GET.get('stat_checkbox')
        for key in request.GET:
            if key != 'stat_checkbox':
                item_checkbox = Product.objects.get(pk=key)
                status_checkbox = Status.objects.get(title=stat_checkbox)
                item_checkbox.status = status_checkbox
                item_checkbox.save()

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

        if filter['date_from'] or filter['date_to']:
            filter.pop('date_from')
            filter.pop('date_to')
        else:
            filter.pop('date_from')
            filter.pop('date_to')

        items = Product.objects.filter(**filter) & Product.objects.filter(
            employee=User.objects.get(username=request.user))
    else:
        items = Product.objects.filter(employee=User.objects.get(username=request.user))

    paid = 0
    items_paid = 0
    for i in items:
        if i.status.pk == 1:
            paid += i.purchase_price
            items_paid += 1

    context = {
        'title': 'Рабочий стол', 'items': items, 'shop': shop, 'stat': status, 'cat': category,
        'formfilter': formfilter, 'client': all_client, 'paid': paid, 'items_paid': items_paid,
    }
    return render(request, 'dashbord/am_dashbord.html', context)


@login_required
def am_client(request, client_id):
    client = get_object_or_404(Client, pk=client_id)
    product = Product.objects.filter(client=client_id, employee=User.objects.get(username=request.user))

    if request.method == 'POST':
        if 'name' in request.POST.keys():
            client.telephone = request.POST.get('telephone')
            client.name = request.POST.get('name')
            client.adress = request.POST.get('adress')
            client.save()
            return redirect('client', client_id=client.pk)

    wait1 = 0
    residue_total_del = 0
    all_product = len(product)
    for p in product:
        wait = datetime.datetime.now().date() - p.time_create.date()
        if wait.days > wait1:
            wait1 = wait.days
        if p.status.title == 'Получено в РФ':
            residue_total_del += p.residue
    context = {'client': client, 'product': product, 'all_product': all_product, 'wait': wait1,
               'residue_total_del': residue_total_del,
               }
    return render(request, 'dashbord/am_client.html', context)


@login_required
def sk(request):
    shop = Shop.objects.all()
    brand = Brand.objects.all()
    goods = Goods.objects.filter(product=None)
    products = Product.objects.filter(Q(status='2') | Q(status='3'))

    if request.method == 'POST':
        good_product = request.POST.dict()
        if 'shop_f' in request.POST.keys():
            good_product.pop('shop_f')
        if 'brand_f' in request.POST.keys():
            good_product.pop('brand_f')
        keys = list(good_product)
        good = Goods.objects.get(pk=keys[1])
        product = Product.objects.get(pk=keys[2])
        good.product = product
        product.status = Status.objects.get(pk=4)
        good.save()
        product.save()

    shop_f = request.GET.get('shop')
    brand_f = request.GET.get('brand')

    if request.GET.get('shop') or request.GET.get('brand'):
        if request.GET.get('shop'):
            try:
                Brand.objects.get(title=request.GET.get('brand_f'))
                filter_brand = Brand.objects.get(title=request.GET.get('brand_f'))
                goods = Goods.objects.filter(Q(product=None) & Q(brand=filter_brand))
                filter_shop = get_object_or_404(Shop, title=request.GET.get('shop'))
                products = products.filter(shop=filter_shop)
            except:
                filter_shop = get_object_or_404(Shop, title=request.GET.get('shop'))
                products = products.filter(shop=filter_shop)
        else:
            try:
                Shop.objects.get(title=request.GET.get('shop_f'))
                filter_shop = Shop.objects.get(title=request.GET.get('shop_f'))
                products = products.filter(shop=filter_shop)
                filter_brand = get_object_or_404(Brand, title=request.GET.get('brand'))
                goods = Goods.objects.filter(Q(product=None) & Q(brand=filter_brand))
            except:
                filter_brand = get_object_or_404(Brand, title=request.GET.get('brand'))
                goods = Goods.objects.filter(Q(product=None) & Q(brand=filter_brand))

    context = {
        'title': 'Рабочий стол', 'goods': goods, 'products': products, 'total_products': len(products),
        'total_goods': len(goods), 'shop': shop, 'brand': brand, 'shop_f': shop_f, 'brand_f': brand_f
    }
    return render(request, 'dashbord/sk.html', context)


@login_required
def sk_batch(request):
    goods = Goods.objects.filter(batch=None)
    brands = Brand.objects.all()

    if request.GET.get('batch'):
        goods = Goods.objects.filter(batch=None)
        if goods:
            weight = goods.aggregate(Sum('weight'))['weight__sum']
            batch = Batch(employee=request.user, weight=weight)
            batch.save()
            for item in goods:
                item.batch = batch
                item.save()
            return redirect('sk_batch')

    if request.method == 'POST':
        if 'description' in request.POST.keys() and 'pk' not in request.POST.keys():
            form = NewGoodsForms(request.POST, request.FILES)
            form_brand = NewBrandForms()
            form.employee = request.user
            if form.is_valid():
                it = form.save(commit=False)
                it.employee = request.user
                it.save()
                return redirect('sk_batch')
        if 'title' in request.POST.keys():
            form_brand = NewBrandForms(request.POST)
            form = NewGoodsForms()
            if form_brand.is_valid():
                form_brand.save()
                return redirect('sk_batch')
        if 'pk' in request.POST.keys():
            good = goods.get(pk=request.POST.get('pk'))
            good.description = request.POST.get('description')
            good.weight = float(request.POST.get('weight').replace(',', '.'))
            brand = Brand.objects.get(title=request.POST.get('brand'))
            good.brand = brand
            good.save()
            return redirect('sk_batch')
    else:
        form = NewGoodsForms()
        form_brand = NewBrandForms()

    context = {
        'title': 'Товар на складе', 'goods': goods, 'form': form, 'form_brand': form_brand, 'brands': brands,
    }
    return render(request, 'dashbord/sk_batch.html', context)


@login_required
def sk_send(request):
    goods = Goods.objects.exclude(product=None)
    goods = goods.exclude(product__status=6)
    text = ''
    if request.GET.keys():
        if 'shipment' in request.GET.keys():
            goods = goods.filter(product__status=5)
            text = f'Всего позиций к отправке {len(goods)} общий вес: ' \
                   f'{goods.aggregate(Sum("weight"))["weight__sum"]} кг.'
        if 'invoice' in request.GET.keys():
            goods = goods.filter(product__status=4).order_by("product__client")
            text = f'Необходимо создать накладные по {len(goods)} позициям для ' \
                   f'{len(goods.values("product__client").annotate(count=Count("product__client")))} клиентов'
        if request.GET.get('stat_checkbox'):
            stat_checkbox = request.GET.get('stat_checkbox')
            for key in request.GET:
                if key != 'stat_checkbox':
                    item_checkbox = Product.objects.get(pk=key)
                    status_checkbox = Status.objects.get(title=stat_checkbox)
                    item_checkbox.status = status_checkbox
                    item_checkbox.save()

    sum_weight = goods.aggregate(Sum('weight'))['weight__sum']
    stat = Status.objects.filter(Q(pk=5) | Q(pk=6))

    context = {
        'title': 'На отправку', 'goods': goods, 'total': len(goods), 'weight': sum_weight, 'text': text, 'stat': stat
    }

    return render(request, 'dashbord/sk_send.html', context)


@login_required
def sk_ceo(request):
    batchs = Batch.objects.filter(shipping=None)

    context = {
        'title': 'Cклад', "batchs": batchs,
    }
    return render(request, 'dashbord/sk_ceo.html', context)
