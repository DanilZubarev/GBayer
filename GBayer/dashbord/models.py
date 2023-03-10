from base.models import *


class Goods(models.Model):
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    image = models.ImageField(upload_to='images_goods/%Y/%m/%d/', verbose_name='Фото')
    description = models.CharField(max_length=200, verbose_name='Описание')
    weight = models.FloatField(verbose_name='Вес')
    brand = models.ForeignKey('Brand', on_delete=models.PROTECT, verbose_name='Бренд')
    shipping = models.IntegerField(null=True, verbose_name='Цена доставки')
    batch = models.ForeignKey('Batch', on_delete=models.CASCADE, null=True, verbose_name='Партия')
    product = models.OneToOneField(Product, on_delete=models.CASCADE, null=True, unique=True)
    employee = models.ForeignKey('auth.User', on_delete=models.CASCADE, verbose_name='Сотрудник')

    class Meta:
        verbose_name = 'Товар на складе'
        verbose_name_plural = 'Товары на складе'
        ordering = ['-time_create']


class Brand(models.Model):
    title = models.CharField(max_length=100, unique=True, verbose_name='Бренд')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Бренд'
        verbose_name_plural = 'Бренды'
        ordering = ['title']


class Batch(models.Model):
    employee = models.ForeignKey('auth.User', null=True, on_delete=models.CASCADE, verbose_name='Сотрудник')
    weight = models.FloatField(null=True, verbose_name='Общий вес')
    shipping = models.IntegerField(null=True, verbose_name='Цена доставки')
    shipping_kg = models.IntegerField(null=True, verbose_name='Цена за кг.')

    def __str__(self):
        return str(self.pk)

    class Meta:
        verbose_name = 'Партия'
        verbose_name_plural = 'Партии'
        ordering = ['pk']
