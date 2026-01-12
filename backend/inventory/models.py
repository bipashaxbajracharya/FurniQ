import re
from django.db import models
from django.contrib.auth.models import User #built-in system for staff
from django.utils import timezone
from datetime import timedelta

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=10)
    
    def __str__(self):
        return f"{self.user.username} - {self.phone_number}"

class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    items_summary = models.TextField() #stores cart detail
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    order_date = models.DateTimeField(auto_now_add=True)
    delivery_date = models.DateTimeField(default=timezone.now() + timedelta(days=3))
    status = models.CharField(max_length=20, default='Pending')
    
    assigned_staff = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={'is_staff': True},
        related_name='staff_orders'
    )
    
    def __str__(self):
        return f"Order {self.id} by {self.customer.username}"

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


class Product(models.Model):
    CATEGORY_CHOICES = [
        ('Bedroom', 'Bedroom'),
        ('Living Room', 'Living Room'),
        ('Dining', 'Dining'),
    ]
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    old_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    stock = models.IntegerField(default=0)
    
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='Living Room')
    
    assigned_staff = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={'is_staff': True}
    )
    
    image = models.ImageField(upload_to='product_images/', null=True, blank=True)
    is_featured = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.name} - {self.category}"