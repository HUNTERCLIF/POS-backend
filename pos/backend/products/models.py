# models.py
from django.db import models


class Product(models.Model):
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    supplier = models.CharField(max_length=255)
    image = models.ImageField(upload_to='product_images/', null=True, blank=True)

    def __str__(self):
        return self.name


class Sale(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    customer_name = models.CharField(max_length=255)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.customer_name} - {self.timestamp}"


class SaleItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def save(self, *args, **kwargs):
        # Update total_amount of the associated sale when saving SaleItem
        self.sale.total_amount += self.product.price * self.quantity
        self.sale.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product} - {self.quantity} units"
