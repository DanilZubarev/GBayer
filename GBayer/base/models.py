from django.db import models
from django.urls import reverse


class Product(models.Model):
    description = models.CharField(max_length=200, verbose_name='Описание')
    image = models.ImageField(upload_to='images/%Y/%m/%d/', verbose_name='Фото')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Время изменения')
    client = models.ForeignKey('Client', on_delete=models.PROTECT, verbose_name='Клиент')
    shop = models.ForeignKey('Shop', on_delete=models.PROTECT, verbose_name='Магазин')
    purchase_price = models.IntegerField(verbose_name='Цена покупки', null=True)
    profit = models.IntegerField(verbose_name='Прибыль', null=True)
    selling_price = models.IntegerField(verbose_name='Цена продажи')
    prepayment = models.IntegerField(verbose_name='Предоплата')
    residue = models.IntegerField(verbose_name='Остаток')
    status = models.ForeignKey('Status', on_delete=models.PROTECT, default=1, verbose_name='Статус')
    category = models.ForeignKey('Category', on_delete=models.PROTECT, default=2, null=True, verbose_name='Категория')
    employee = models.ForeignKey('auth.User', null=True, on_delete=models.CASCADE, verbose_name='Сотрудник')
    have = models.BooleanField(default=False, verbose_name='Наличие')

    def get_absolute_url(self):
        return reverse('product', kwargs={'product_id': self.pk})

    def save(self, *args, **kwargs):
        if not self.residue:
            self.residue = self.selling_price - self.prepayment
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['-time_create']


class Client(models.Model):
    telephone = models.CharField(max_length=12, unique=True, verbose_name='Телефон')
    name = models.CharField(max_length=100, verbose_name='ФИО', null=True)
    adress = models.CharField(max_length=300, verbose_name='Адресс', null=True)

    def get_absolute_url(self):
        return reverse('client', kwargs={'client_id': self.pk})

    def __str__(self):
        return self.telephone

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


class Shop(models.Model):
    title = models.CharField(max_length=100, unique=True, verbose_name='Магазин')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Магазин'
        verbose_name_plural = 'Магазины'
        ordering = ['title']


class Status(models.Model):
    title = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Статус'
        verbose_name_plural = 'Статусы'
        ordering = ['pk']


class Category(models.Model):
    title = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Rate(models.Model):
    usd = models.FloatField(verbose_name='USD')
    eur = models.FloatField(verbose_name='EUR')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Время изменения')

    class Meta:
        verbose_name = 'Курс валют'
        verbose_name_plural = 'Курс валют'


