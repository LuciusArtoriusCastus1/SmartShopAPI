from django.contrib import admin
from django.utils.safestring import mark_safe

from customuser.models import User, Genders


class UserConfig(admin.ModelAdmin):
    list_display = ('id', 'display_name', 'email', 'get_profile_image', 'gender', 'join_date', 'is_staff', 'seller_status')
    list_display_links = ('display_name',)
    ordering = ('display_name', 'join_date')
    search_fields = ('display_name', 'bio')
    list_editable = ('is_staff', 'seller_status',)
    list_filter = ('is_active', 'is_staff', 'seller_status', 'join_date')
    readonly_fields = ('join_date',)
    save_on_top = True

    def get_profile_image(self, obj):
        if obj.profile_image:
            return mark_safe(f"<img src='{obj.profile_image.url}' width=70 style='border-radius: 100px;'>")

    get_profile_image.short_description = 'Profile Image'


class GendersConfig(admin.ModelAdmin):
    list_display = ('gender', )


admin.site.register(User, UserConfig)
admin.site.register(Genders, GendersConfig)
