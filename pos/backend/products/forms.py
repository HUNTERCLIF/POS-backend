# products/forms.py
from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['code', 'name', 'price', 'quantity', 'supplier', 'image']


class SaleForm(forms.Form):
    quantity_sold = forms.IntegerField(min_value=1)