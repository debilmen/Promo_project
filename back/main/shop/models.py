from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager
from django.db import models
from datetime import datetime
from django.conf import settings
from mptt.models import MPTTModel, TreeForeignKey


class UserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None, is_staff=False, is_superuser=False, is_active=True):

        if not email:
            raise ValueError('Users must have an email address')

        if not password:
            raise ValueError('Must have pas')

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name
        )
        user.is_staff = is_staff
        user.is_superuser = is_superuser
        user.is_active = is_active
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, first_name, last_name, password=None):
        user = self.create_user(
            email,
            first_name=first_name,
            last_name=last_name,
            password=password,
            is_staff=True,
        )
        return user

    def create_superuser(self, email, first_name, last_name, password=None):

        user = self.create_user(
            email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            is_superuser=True,
            is_staff=True
        )
        return user


class User(AbstractBaseUser):
    """
    Пользователь
    """

    first_name = models.CharField("Имя", max_length=100)
    last_name = models.CharField("Фамилия", max_length=100)
    email = models.EmailField("Почта", unique=True)
    password = models.CharField("Пароль", max_length=100)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    objects = UserManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def staff(self):
        return self.is_staff

    @property
    def superuser(self):
        return self.is_superuser

    @property
    def active(self):
        return self.is_active

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Categories(MPTTModel):
    """
    Категории
    """
    user_id = models.ForeignKey(
        User, verbose_name="Пользователь", on_delete=models.CASCADE
    )
    name = models.CharField("Категория", max_length=100)
    parent = TreeForeignKey(
        'self', verbose_name="Категория", on_delete=models.CASCADE, blank=True, null=True
    )

    def __str__(self):
        return self.name

    class MPTTMeta:
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
        User, verbose_name="Пользователь", on_delete=models.CASCADE
    )

    def __str__(self):
        return self.type

    class Meta:
        verbose_name = "Транзакция"
        verbose_name_plural = "Транзакции"
