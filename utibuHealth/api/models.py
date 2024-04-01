from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)
# Create your models here
class Dosage(models.Model):
    name= models.CharField(max_length=100,blank=True)
    description = models.TextField()
    price= models.FloatField()
    image = models.FileField(upload_to='files/dosage', blank=True, max_length=255)
    qty = models.IntegerField(default=0)
    
    def __str__(self) -> str:
        return str(self.name)
    
class Order(models.Model):
    delivery_choices = (
        ('Deliver to my address', 'Deliver to my address'),
        ('Pick from pharmacy', 'Pick from pharmacy')
    )
    status_choices = (
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed')
    )
    payment_choices =(
        ('On Delivery', "On Delivery"),
        ("On Order", "On Order")
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cart_item = models.ManyToManyField('CartItem', related_name='orders', blank=True, null=True)
    delivery_method = models.CharField(choices=delivery_choices, default='Pick from pharmacy', max_length=200)
    status = models.CharField(choices=status_choices, default='In Progress', max_length=20)
    payment = models.CharField(choices=payment_choices, blank=True, null=True, max_length=20)
    paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return str(f'{self.user} - Order')

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    dosage = models.ForeignKey(Dosage, on_delete=models.CASCADE, related_name='cart_item', blank=True, null=True)
    qty = models.IntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)
    checked = models.BooleanField(default=False)

    def __str__(self) -> str:
        return str(f'{self.user} -  Cart Item -> {str(self.dosage)}')
    