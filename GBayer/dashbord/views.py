from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User


from base.form import *



@login_required
def am(request, name):

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

        items = Product.objects.filter(**filter) & Product.objects.filter(employee=User.objects.get(username=name))
    else:
        items = Product.objects.filter(employee=User.objects.get(username=name))

    context = {
        'title': 'Base', 'items': items, 'shop': shop, 'stat': status, 'cat': category,
        'formfilter': formfilter, 'client': all_client,
    }

    return render(request, 'dashbord/am_dashbord.html', context)
