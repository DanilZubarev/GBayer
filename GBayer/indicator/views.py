from datetime import datetime, timedelta
import calendar

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.db.models import Q, Sum, Count

from base.models import *


@login_required
def indicator_general(request):
    items = Product.objects.all()
    current_date = datetime.now()

    start_date = datetime(current_date.year, current_date.month, 1)
    end_date = start_date + timedelta(days=calendar.monthrange(start_date.year, start_date.month)[1])
    items_current_month = items.filter(Q(time_update__gte=start_date) & Q(time_update__lte=end_date))
    profit_current_month = items_current_month.aggregate(Sum("profit"))["profit__sum"]

    last_month = current_date.month - 1 if current_date.month > 1 else 12
    year_last_month = datetime.now().year if current_date.month > 1 else datetime.now().year - 1
    start_date = datetime(year_last_month, last_month, 1)
    end_date = start_date + timedelta(days=calendar.monthrange(start_date.year, start_date.month)[1])
    items_last_month = items.filter(Q(time_update__gte=start_date) & Q(time_update__lte=end_date))
    profit_last_month = items_last_month.aggregate(Sum("profit"))["profit__sum"]

    context = {'profit_last_month': profit_last_month, 'profit_current_month': profit_current_month,
               'product_current_month': len(items_current_month), 'product_last_month': len(items_last_month),

    }
    return render(request, 'indicator/indicator_general.html', context)

