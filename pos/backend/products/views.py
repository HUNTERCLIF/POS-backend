# products/views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import Product
from .forms import ProductForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Product, SaleItem, Sale  
from .forms import ProductForm, SaleForm
from django.db.models import Sum, F
from  rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


@login_required
def product_list(request):
    products = Product.objects.all()
    return render(request, 'store/product_list.html', {'products': products})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        sale_form = SaleForm(request.POST)
        if sale_form.is_valid():
            quantity_sold = sale_form.cleaned_data['quantity_sold']
            Sale.objects.create(product=product, quantity_sold=quantity_sold)
            return redirect('product_list')
    else:
        sale_form = SaleForm()

    return render(request, 'store/product_detail.html', {'product': product, 'sale_form': sale_form})

def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'store/product_form.html', {'form': form, 'action': 'Create'})

def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'store/product_form.html', {'form': form, 'action': 'Update'})

def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('product_list')
    return render(request, 'store/product_confirm_delete.html', {'product': product})


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            login(request, user)
            return redirect('product_list')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


def sales_reports(request):
    # Example query: Get total sales quantity and amount per product
    sales_data = SaleItem.objects.values('product__name').annotate(
        total_quantity=Sum('quantity'),
        total_amount=Sum('quantity' * F('product__price'))  # Use F instead of models.F
    )

    # Prepare data for Chart.js
    product_names = [item['product__name'] for item in sales_data]
    total_quantities = [item['total_quantity'] for item in sales_data]
    total_amounts = [item['total_amount'] for item in sales_data]

    # Pass data to template
    context = {
        'product_names': product_names,
        'total_quantities': total_quantities,
        'total_amounts': total_amounts,
    }

    return render(request, 'registration/sales_reports.html', context)


