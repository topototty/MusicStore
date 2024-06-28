from django import forms
from django.core.validators import MaxLengthValidator, MinLengthValidator, RegexValidator

from .models import *
class DefaultForm(forms.Form):
    name = forms.CharField(
        max_length=50,
        label='ФОРМА',
        strip=True,
        widget=forms.TextInput(
            attrs={
                "class":"form-control"
            }
        )
    )

    description = forms.CharField(
        label='Описание',
        strip=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )

    tf = forms.BooleanField(
        label='труфолс',
    )

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'photo', 'category', 'tags']
        widgets = {
            'name': forms.TextInput(attrs={"class": "form-control"}),
            'description': forms.TextInput(attrs={"class": "form-control"}),
            'price': forms.NumberInput(attrs={"class": "form-control"}),
            'photo': forms.FileInput(attrs={"class": "form-control"}),
            'category': forms.Select(attrs={"class": "form-control"}),
            'tags': forms.SelectMultiple(attrs={"class": "form-control"}),
        }

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={"class": "form-control"}),
            'description': forms.TextInput(attrs={"class": "form-control"}),
        }

class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={"class": "form-control"}),
            'description': forms.TextInput(attrs={"class": "form-control"}),
        }

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['delivery_address', 'client_phone', 'client_name',]
        widgets = {
            'delivery_address': forms.TextInput(attrs={"class": "form-control"}),
            'client_phone': forms.NumberInput(attrs={"class": "form-control"}),
            'client_name': forms.TextInput(attrs={"class": "form-control"}),
        }