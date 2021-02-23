from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser, User
from django.db import models
from datetime import datetime
from django.conf import settings

class MyUserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class MyUser(AbstractUser):
    """
    Пользователь
    """

    first_name = models.CharField("Имя", max_length=100)
    last_name = models.CharField("Фамилия", max_length=100)
    email = models.EmailField("Почта", unique=True)
    password = models.CharField("Пароль", max_length=100)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    objects = MyUserManager()
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
        settings.AUTH_USER_MODEL, verbose_name="Пользователь", on_delete=models.CASCADE
    )
    name = models.CharField("Категория", max_length=100)
    parent_id = models.ForeignKey(
        'self', verbose_name="Категория", on_delete=models.CASCADE, blank=True, null=True
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
    type = models.CharField("Тип", max_length=100)
    amount = models.FloatField("Количество")
    comment = models.TextField("Коментарий")
    date = models.DateTimeField("Дата", default=datetime.now())
    category_id = models.ForeignKey(
        Categories, verbose_name="Категория", on_delete=models.CASCADE
    )
    user_id = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name="Пользователь", on_delete=models.CASCADE
    )

    def __str__(self):
        return self.type

    class Meta:
        verbose_name = "Транзакция"
        verbose_name_plural = "Транзакции"
