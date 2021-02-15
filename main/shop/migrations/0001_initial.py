# Generated by Django 3.1.6 on 2021-02-15 09:10

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Categories',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Фамилия')),
                ('parent_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.categories', verbose_name='Категория')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100, verbose_name='Имя')),
                ('last_name', models.CharField(max_length=100, verbose_name='Фамилия')),
                ('email', models.EmailField(max_length=254, verbose_name='Почта')),
                ('password', models.CharField(max_length=100, verbose_name='Пароль')),
            ],
            options={
                'verbose_name': 'Пользователь',
                'verbose_name_plural': 'Пользователи',
            },
        ),
        migrations.CreateModel(
            name='Transactions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=100, verbose_name='Имя')),
                ('amount', models.FloatField(verbose_name='Количество')),
                ('comment', models.TextField(verbose_name='Коментарий')),
                ('date', models.DateTimeField(default=datetime.datetime(2021, 2, 15, 14, 10, 27, 288952), verbose_name='Дата')),
                ('category_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.categories', verbose_name='Категория')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.user', verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Транзакция',
                'verbose_name_plural': 'Транзакции',
            },
        ),
        migrations.AddField(
            model_name='categories',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.user', verbose_name='Пользователь'),
        ),
    ]