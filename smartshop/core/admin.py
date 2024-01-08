from django.contrib import admin
from .models import Cart


class CartConfig(admin.ModelAdmin):
    list_display = ('id', 'owner', 'product')
    list_filter = ('owner', 'product')


admin.site.register(Cart, CartConfig)
