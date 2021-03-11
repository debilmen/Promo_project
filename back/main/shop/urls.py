from django.contrib.auth.views import LoginView
from django.urls import path

from .views import (
    index, RegisterView, LoginView, LogoutView,
    CreateCategory, UpdateCategory, DeleteCategory, GetCategories, GetTransaction, CreateTransaction, UpdateTransaction,
    DeleteTransaction
)
urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('', index, name='index'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('categories/', GetCategories.by_category, name='get_categories'),
    path('categories/create/', CreateCategory.as_view(), name='create_category'),
    path('categories/patch/<int:pk>/', UpdateCategory.as_view(),  name='patch_category'),
    path('categories/delete/<int:pk>/', DeleteCategory.as_view(), name='delete_category'),
    path('transactions/', GetTransaction.get_transactions, name='get_transactions'),
    path('transactions/<int:pk>/', GetTransaction.info_transaction, name='info_transaction'),
    path('transactions/create', CreateTransaction.as_view(), name='create_transaction'),
    path('transactions/patch/<int:pk>/', UpdateTransaction.as_view(), name='patch_transaction'),
    path('transactions/delete/<int:pk>/', DeleteTransaction.as_view(), name='delete_transaction'),
]