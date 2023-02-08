import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User


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

        items = Product.objects.filter(**filter) & Product.objects.filter(employee=User.objects.get(username=request.user))
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
            return redirect('client', client_id=client.pk )

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
    goods = Goods.objects.all()

    if request.method == 'POST':
        if 'description' in request.POST.keys():
            form = NewGoodsForms(request.POST, request.FILES)
            form_brand = NewClientForms()
            form.employee = request.user
            if form.is_valid():
                it = form.save(commit=False)
                it.employee = request.user
                it.save()
                return redirect('sk')
        if 'title' in request.POST.keys():
            form_brand = NewBrandForms(request.POST)
            form = NewGoodsForms()
            if form_brand.is_valid():
                form_brand.save()
                return redirect('sk')
    else:
        form = NewGoodsForms()
        form_brand = NewClientForms()

    context = {
        'title': 'Рабочий стол', 'goods': goods, 'form': form, 'form_brand': form_brand
    }
    return render(request, 'dashbord/sk_dashbord.html', context)
