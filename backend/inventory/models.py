from django.db import models
from django.contrib.auth.models import User #built-in system for staff

# Create your models here.
class Product(models.Model):
    CATEGORY_CHOICES = [
        ('Bedroom', 'Bedroom'),
        ('Living Room', 'Living Room'),
        ('Dining', 'Dining'),
    ]
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
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
    
    def __str__(self):
        return f"{self.name} - {self.category}"