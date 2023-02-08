from django import forms

from .models import *


class NewGoodsForms(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['brand'].empty_label = 'Выбери из списка'

    class Meta:
        model = Goods
        fields = ['description', 'image', 'weight', 'brand', 'shipping', 'batch',]
        widgets = {
            'description': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Описание товара: характеристика, цвет, размер и т.п.'}),
            'image': forms.FileInput(attrs={'class': 'form-control form-control'}),
            'brand': forms.Select(attrs={'class': 'form-select'}),
            'weight': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Вес в граммах'}),
        }


class NewBrandForms(forms.ModelForm):
    class Meta:
        model = Brand
        fields = ['title']
        widgets = {'title': forms.TextInput(attrs={'class': 'form-control shadow-sm', 'placeholder': 'Введи название бренда'})}
