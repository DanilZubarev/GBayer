# Generated by Django 4.1.5 on 2023-01-21 18:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_auto_20230109_2253'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='shop',
            options={'ordering': ['title'], 'verbose_name': 'Магазин', 'verbose_name_plural': 'Магазины'},
        ),
        migrations.AlterModelOptions(
            name='status',
            options={'ordering': ['pk'], 'verbose_name': 'Статус', 'verbose_name_plural': 'Статусы'},
        ),
        migrations.AlterField(
            model_name='category',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='client',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='product',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='product',
            name='prepayment',
            field=models.IntegerField(default=0, verbose_name='Предоплата'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='product',
            name='purchase_price',
            field=models.IntegerField(null=True, verbose_name='Цена покупки'),
        ),
        migrations.AlterField(
            model_name='product',
            name='residue',
            field=models.IntegerField(default=0, verbose_name='Остаток'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='shop',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='status',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]