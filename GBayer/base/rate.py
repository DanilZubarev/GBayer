import datetime

from bs4 import BeautifulSoup
import requests

from .models import Rate


def rate():
    url_kz = 'https://banks.kg/bank/bank-bay-tushum/rates'
    html = requests.get(url_kz).text

    soup = BeautifulSoup(html, 'lxml')
    ul = soup.find('ul', class_='rates__board')
    rate_list = []
    for i in ul:
        div = i.find('div')
        if type(div) != int:
            rate_list.extend(div.text.split())
    rate_now = {
        'usd': format(float(rate_list[1]) / float(rate_list[4]), '.2f'),
        'eur': format((float(rate_list[1]) / float(rate_list[4])) * (float(rate_list[3]) / float(rate_list[0])), '.2f'),
    }

    if Rate.objects.latest('id').usd != float(rate_now['usd']) and Rate.objects.latest('id').eur != float(rate_now['eur']):
        rate_object = Rate(usd=rate_now['usd'], eur=rate_now['eur'])
        rate_object.save()
    else:
        Rate.objects.latest('id').time_update = datetime.datetime.now()
        Rate.objects.latest('id').save()
