from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import *


class ProductCategoryConfig(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name', )}
    list_display = ('name', )
    list_display_links = ('name',)


class AttachmentsConfig(admin.ModelAdmin):
    list_display = ('id', 'product', 'get_product_image')
    list_display_links = ('id',)

    def get_product_image(self, obj):
        if obj.photo:
            return mark_safe(f"<img src='{obj.photo.url}' width=70 style='border-radius: 10px;'>")


class RatingStarConfig(admin.ModelAdmin):
    list_display = ('star',)


class RatingConfig(admin.ModelAdmin):
    list_display = ('id', 'rate', 'product', 'owner', 'post_date', 'changed')
    list_display_links = ('id',)


class ProductsConfig(admin.ModelAdmin):
    list_display = ('id', 'name', 'rate', 'price', 'category', 'get_product_image', 'amount', 'sold', 'owner', 'post_date')
    list_display_links = ('name',)
    ordering = ('post_date', 'name', 'price')
    search_fields = ('name', 'description')
    list_filter = ('price', 'amount', 'sold', 'post_date', 'owner')
    readonly_fields = ('post_date', 'rate')
    prepopulated_fields = {'slug': ('name', )}
    save_on_top = True

    def get_product_image(self, obj):
        if obj.photo:
            return mark_safe(f"<img src='{obj.photo.url}' width=70 style='border-radius: 10px;'>")

    get_product_image.short_description = 'Product Image'


admin.site.register(Products, ProductsConfig)
admin.site.register(ProductCategory, ProductCategoryConfig)
'''------------------------------------------'''
admin.site.register(Attachments, AttachmentsConfig)
admin.site.register(RatingStar, RatingStarConfig)
admin.site.register(Rating, RatingConfig)
'''------------------------------------------'''
admin.site.register(LaptopBrand)
admin.site.register(LaptopProcessor)
admin.site.register(LaptopRAM)
admin.site.register(LaptopDescreteGraficsCard)
admin.site.register(LaptopOperatingSystem)
admin.site.register(LaptopSSDCapacity)
admin.site.register(MadeIn)
admin.site.register(LaptopViedoCardMemoryCapacity)
admin.site.register(LaptopScreenType)
admin.site.register(LaptopProcessorCores)
admin.site.register(LaptopVideoCardType)
admin.site.register(LaptopDriveType)
admin.site.register(LaptopRAMType)
admin.site.register(LaptopResolution)
admin.site.register(LaptopBatteryCapacity)
admin.site.register(LaptopScreenRefreshRate)
admin.site.register(ManufactureYear)
admin.site.register(Color)
admin.site.register(TabletBrand)
admin.site.register(TabletRAM)
admin.site.register(TabletBuiltInMemory)
admin.site.register(TabletWirelessCapabilities)
admin.site.register(TabletOperatingSystem)
admin.site.register(TabletMatrixType)
admin.site.register(TabletFeatures)
admin.site.register(TabletScreenResolution)
admin.site.register(TabletProcessorCores)
admin.site.register(TabletProcessor)
admin.site.register(TabletMainCamera)
admin.site.register(TabletFrontCamera)
admin.site.register(PhoneBrand)
admin.site.register(PhoneRAM)
admin.site.register(PhoneBuiltInMemory)
admin.site.register(PhoneMemoryCapacity)
admin.site.register(PhoneWirelessTechnologies)
admin.site.register(PhoneMainCameraMP)
admin.site.register(PhoneMainCameraFeatures)
admin.site.register(PhoneFrontCameraMP)
admin.site.register(PhoneProcessorName)
admin.site.register(PhoneDisplayResolution)
admin.site.register(PhoneMatrixType)
admin.site.register(PhoneScreenRefreshRate)
admin.site.register(PhoneOperatingSystem)
admin.site.register(PhoneEquipment)
admin.site.register(NumberOfSIMCards)

