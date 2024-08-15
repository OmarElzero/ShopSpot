# forms.py

from django import forms
from django.contrib.auth.models import User
from .models import Customer



class ProductSearchForm(forms.Form):
    search_query = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'placeholder': 'Search...'}))


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Customer
        fields = ('name', 'email', 'phone', 'address', 'username', 'password', 'confirm_password')

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already exists.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists.")
        return email

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if Customer.objects.filter(phone=phone).exists():
            raise forms.ValidationError("Phone number already exists.")
        return phone

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")

        return cleaned_data