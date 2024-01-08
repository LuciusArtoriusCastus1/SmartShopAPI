from django.contrib import admin

from reviews.models import Like, Reviews


class LikeConfig(admin.ModelAdmin):
    list_display = ('liked', 'review', 'owner')


class ReviewsConfig(admin.ModelAdmin):
    list_display = ('id', 'likes', 'text', 'refers_to', 'product', 'owner', 'post_date')
    list_display_links = ('id', )


admin.site.register(Like, LikeConfig)
admin.site.register(Reviews, ReviewsConfig)
