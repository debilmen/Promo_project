from django.db import models
from datetime import datetime


class User(models.Model):
    """
    Пользователь
    """
    first_name = models.CharField("Имя", max_length=100)
    last_name = models.CharField("Фамилия", max_length=100)
    email = models.EmailField("Почта")
    password = models.CharField("Пароль", max_length=100)

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Categories(models.Model):
    """
    Категории
    """
    user_id = models.ForeignKey(
        User, verbose_name="Пользователь", on_delete=models.CASCADE
    )
    name = models.CharField("Фамилия", max_length=100)
    parent_id = models.ForeignKey(
        'self', verbose_name="Категория", on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Transactions(models.Model):
    """
    Транзакции
    """
    type = models.CharField("Имя", max_length=100)
    amount = models.FloatField("Количество")
    comment = models.TextField("Коментарий")
    date = models.DateTimeField("Дата", default=datetime.now())
    category_id = models.ForeignKey(
        Categories, verbose_name="Категория", on_delete=models.SET_NULL
    )
    user_id = models.ForeignKey(
        User, verbose_name="Пользователь", on_delete=models.SET_NULL
    )

    def __str__(self):
        return self.type

    class Meta:
        verbose_name = "Транзакция"
        verbose_name_plural = "Транзакции"
