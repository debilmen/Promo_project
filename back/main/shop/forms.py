from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import User, Categories, Transactions


class RegisterForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(RegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password', 'is_active', 'is_superuser', )

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class LoginForm(forms.Form):
    email = forms.EmailField(label='Email')
    password = forms.CharField(widget=forms.PasswordInput)


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Categories
        fields = ['name', 'parent']

    def __init__(self, *args, **kwargs):
        self.user_id = kwargs.pop('user_id')
        super(CategoryForm, self).__init__(*args, **kwargs)
        self.fields['parent'].queryset = Categories.objects.filter(user_id=self.user_id)


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transactions
        fields = ['type', 'amount', 'comment', 'date', 'category_id']

    def __init__(self, *args, **kwargs):
        self.user_id = kwargs.pop('user_id')
        super(TransactionForm, self).__init__(*args, **kwargs)
        self.fields['category_id'].queryset = Categories.objects.filter(user_id=self.user_id)


