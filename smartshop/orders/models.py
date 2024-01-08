from django.db import models

from customuser.models import User
from products.models import Products


class Orders(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name='orders')
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    quantity = models.PositiveIntegerField()
    total_price = models.PositiveIntegerField()
    destination = models.ForeignKey('PostOffices', on_delete=models.CASCADE, related_name='orders')
    order_date = models.DateTimeField(auto_now_add=True)
    sent = models.BooleanField(default=False)
    sent_date = models.DateTimeField(blank=True, null=True)
    delivered = models.BooleanField(default=False)
    delivery_date = models.DateTimeField(blank=True, null=True)
    paid_up = models.BooleanField(default=False)
    pay_date = models.DateTimeField(blank=True, null=True)
    declined = models.BooleanField(default=False)
    decline_date = models.DateTimeField(blank=True, null=True)
    decline_description = models.TextField(max_length=500, blank=True, null=True)

    def __str__(self):
        return f'{self.product}-{self.customer}-{self.quantity}'


class PostOffices(models.Model):
    address = models.CharField(max_length=300)

    def __str__(self):
        return self.address
