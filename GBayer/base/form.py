from django import forms

from .models import *


class NewProductForms(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['shop'].empty_label = 'Выбери из списка'

    class Meta:
        model = Product
        fields = ['description', 'image', 'client', 'shop', 'purchase_price', 'selling_price', 'prepayment', 'category']
        widgets = {
            'description': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Описание товара: характеристика, цвет, размер и т.п.'}),
            'image': forms.FileInput(attrs={'class': 'form-control form-control'}),
            'client': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Введите для поиска...', 'list': 'listClient'}),
            'shop': forms.Select(attrs={'class': 'form-select'}),
            'purchase_price': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Цена покупки в рублях'}),
            'selling_price': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Цена продажи'}),
            'prepayment': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Сумма предоплаты'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
        }


class NewClientForms(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['telephone', 'name', 'adress']
        widgets = {
            'telephone': forms.TextInput(attrs={'class': 'form-control shadow-sm', 'placeholder': 'Введи телефон с 8....'}),
            'name': forms.TextInput(attrs={'class': 'form-control shadow-sm', 'placeholder': 'Введи ФИО'}),
            'adress': forms.TextInput(attrs={'class': 'form-control shadow-sm', 'placeholder': 'Введи Адрес'}),
        }


class NewShopForms(forms.ModelForm):
    class Meta:
        model = Shop
        fields = ['title']
        widgets = { 'title': forms.TextInput(attrs={'class': 'form-control shadow-sm', 'placeholder': 'Введи название магазина'})}


class FilterForms(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['shop'].empty_label = 'Ничего не выбрано'
        self.fields['cat'].empty_label = 'Ничего не выбрано'
        self.fields['stat'].empty_label = 'Ничего не выбрано'

    shop = forms.ModelChoiceField(
        queryset=Shop.objects.all(), to_field_name="title", required=False,
        widget=forms.Select(attrs={'class': 'form-control'}), label="Магазин"
    )
    cat = forms.ModelChoiceField(
        queryset=Category.objects.all(), to_field_name="title", required=False,
        widget=forms.Select(attrs={'class': 'form-control'}), label="Категория"
    )
    stat = forms.ModelChoiceField(
        queryset=Status.objects.all(), to_field_name="title", required=False,
        widget=forms.Select(attrs={'class': 'form-control'}), label="Статус"
    )
