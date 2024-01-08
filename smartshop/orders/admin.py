from django.contrib import admin

from orders.models import Orders, PostOffices


class OrdersConfig(admin.ModelAdmin):
    list_display = ('id', 'product', 'customer', 'quantity', 'total_price', 'destination', 'paid_up', 'declined')
    list_filter = ('product', 'total_price', 'destination', 'paid_up')
    list_display_links = ('id', )
    ordering = ('total_price', 'order_date')
    search_fields = ('product',)
    readonly_fields = ('order_date', 'sent_date', 'delivery_date', 'pay_date')
    save_on_top = True


class PostOfficesConfig(admin.ModelAdmin):
    list_display = ('id', 'address')
    search_fields = ('address',)


admin.site.register(Orders, OrdersConfig)
admin.site.register(PostOffices, PostOfficesConfig)

