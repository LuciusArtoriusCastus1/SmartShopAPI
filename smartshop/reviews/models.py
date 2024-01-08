from django.db import models

from customuser.models import User
from products.models import Products


class Like(models.Model):
    liked = models.BooleanField(default=False)
    review = models.ForeignKey('Reviews', on_delete=models.CASCADE, related_name='like')
    owner = models.ForeignKey(User, on_delete=models.CASCADE)


class Reviews(models.Model):
    likes = models.PositiveIntegerField(default=0)
    text = models.CharField(max_length=300)
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name='reviews')
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    post_date = models.DateField(auto_now_add=True)
    refers_to = models.ForeignKey('self', models.CASCADE, blank=True, null=True, related_name='referred_by')

    class Meta:
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'

    def __str__(self):
        return str(self.id)


