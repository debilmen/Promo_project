from django.contrib import admin
from .models import User, Categories, Transactions

admin.site.register(User)
admin.site.register(Categories)
admin.site.register(Transactions)
