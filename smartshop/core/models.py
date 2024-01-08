from django.db import models

from django.db import models
from products.models import Products
from customuser.models import User


class Cart(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)

