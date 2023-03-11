from datetime import datetime, timedelta

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.db.models import Q, Sum, Count


@login_required
def indicator_general(request):

    context = {

    }
    return render(request, 'indicator/indicator_general.html', context)

