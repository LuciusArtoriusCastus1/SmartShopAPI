from django.core.validators import FileExtensionValidator
from django.db import models
from django.db.models import Avg
from django.utils.text import slugify
from datetime import date, timedelta
from customuser.models import User
from .services import get_product_photo, get_attachment_photo, get_product_video


class Attachments(models.Model):
    product = models.ForeignKey('Products', on_delete=models.CASCADE, related_name='attachments')
    photo = models.ImageField(
        blank=True, null=True,
        upload_to=get_attachment_photo,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'png'])],
    )


class RatingStar(models.Model):
    star = models.PositiveIntegerField()

    def __str__(self):
        return str(self.star)

    class Meta:
        verbose_name = 'RatingStar'
        verbose_name_plural = 'RatingStars'


class Rating(models.Model):
    rate = models.ForeignKey('RatingStar', on_delete=models.CASCADE)
    product = models.ForeignKey('Products', on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    post_date = models.DateField(auto_now_add=True)
    changed = models.DateField(auto_now=True)

    def __str__(self):
        return str(self.rate)

    class Meta:
        verbose_name = 'Rating'
        verbose_name_plural = 'Ratings'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        item = Products.objects.get(id=self.product.id)
        rate = item.rating_set.aggregate(rating=Avg('rate'))

        if rate['rating']:
            item.rate = round(float(rate['rating']), 2)
            item.save()

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)

        item = Products.objects.get(id=self.product.id)
        rate = item.rating_set.aggregate(rating=Avg('rate'))

        if rate['rating']:
            item.rate = round(float(rate['rating']), 2)
            item.save()
        else:
            item.rate = rate['rating']
            item.save()


class BaseProductModel(models.Model):
    slug = models.SlugField(max_length=50, db_index=True, unique=True)
    name = models.CharField(max_length=50, db_index=True)
    category = models.ForeignKey('ProductCategory', on_delete=models.CASCADE, blank=True, null=True)
    made_in = models.ForeignKey('MadeIn', on_delete=models.CASCADE, blank=True, null=True)
    photo = models.ImageField(
        blank=True, null=True,
        upload_to=get_product_photo,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'png'])],
    )
    video = models.FileField(
        blank=True, null=True,
        upload_to=get_product_video,
        validators=[FileExtensionValidator(allowed_extensions=['mp4'])],
    )
    price = models.FloatField()
    screen_diagonal = models.FloatField(blank=True, null=True)
    weight = models.FloatField(blank=True, null=True)
    manufacture_year = models.ForeignKey('ManufactureYear', on_delete=models.CASCADE, blank=True, null=True)
    color = models.ForeignKey('Color', on_delete=models.CASCADE, blank=True, null=True)
    discount = models.FloatField(blank=True, null=True)
    amount = models.PositiveIntegerField()
    sold = models.PositiveIntegerField(default=0)
    description = models.TextField(max_length=300)
    post_date = models.DateField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    rate = models.FloatField(blank=True, null=True, default=None)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)

        super().save(*args, **kwargs)


class Products(BaseProductModel, models.Model):
    laptop_brand = models.ForeignKey('LaptopBrand', on_delete=models.CASCADE, blank=True, null=True)
    laptop_processor = models.ForeignKey('LaptopProcessor', on_delete=models.CASCADE, blank=True, null=True)
    laptop_ram = models.ForeignKey('LaptopRAM', on_delete=models.CASCADE, blank=True, null=True)
    laptop_descrete_grafics_card = models.ForeignKey('LaptopDescreteGraficsCard', on_delete=models.CASCADE, blank=True, null=True)
    laptop_operating_system = models.ForeignKey('LaptopOperatingSystem', on_delete=models.CASCADE, blank=True, null=True)
    laptop_sssd_capacity = models.ForeignKey('LaptopSSDCapacity', on_delete=models.CASCADE, blank=True, null=True)
    laptop_video_card_memory_capacity = models.ForeignKey('LaptopViedoCardMemoryCapacity', on_delete=models.CASCADE, blank=True, null=True)
    laptop_screentype = models.ForeignKey('LaptopScreenType', on_delete=models.CASCADE, blank=True, null=True)
    laptop_processor_cores = models.ForeignKey('LaptopProcessorCores', on_delete=models.CASCADE, blank=True, null=True)
    laptop_videocard_type = models.ForeignKey('LaptopVideoCardType', on_delete=models.CASCADE, blank=True, null=True)
    laptop_drive_type = models.ForeignKey('LaptopDriveType', on_delete=models.CASCADE, blank=True, null=True)
    laptop_ram_type = models.ForeignKey('LaptopRAMType', on_delete=models.CASCADE, blank=True, null=True)
    laptop_resolution = models.ForeignKey('LaptopResolution', on_delete=models.CASCADE, blank=True, null=True)
    laptop_battery_capacity = models.ForeignKey('LaptopBatteryCapacity', on_delete=models.CASCADE, blank=True, null=True)
    laptop_screen_refresh_rate = models.ForeignKey('LaptopScreenRefreshRate', on_delete=models.CASCADE, blank=True, null=True)
    '''--------------------------------------------------------------------------------------------------------------'''
    number_of_sim_cards = models.PositiveIntegerField(null=True, blank=True)
    '''--------------------------------------------------------------------------------------------------------------'''
    tablet_brand = models.ForeignKey('TabletBrand', on_delete=models.CASCADE, null=True, blank=True)
    tablet_ram = models.ForeignKey('TabletRAM', on_delete=models.CASCADE, null=True, blank=True)
    tablet_built_in_memory = models.ForeignKey('TabletBuiltInMemory', on_delete=models.CASCADE, null=True, blank=True)
    tablet_wireless_capabilities = models.ForeignKey('TabletWirelessCapabilities', on_delete=models.CASCADE, null=True, blank=True)
    tablet_operating_system = models.ForeignKey('TabletOperatingSystem', on_delete=models.CASCADE, null=True, blank=True)
    tablet_matrix_type = models.ForeignKey('TabletMatrixType', on_delete=models.CASCADE, null=True, blank=True)
    tablet_features = models.ManyToManyField('TabletFeatures', blank=True)
    tablet_screen_resolution = models.ForeignKey('TabletScreenResolution', on_delete=models.CASCADE, null=True, blank=True)
    tablet_processor_cores = models.ForeignKey('TabletProcessorCores', on_delete=models.CASCADE, null=True, blank=True)
    tablet_processor = models.ForeignKey('TabletProcessor', on_delete=models.CASCADE, null=True, blank=True)
    tablet_main_camera = models.ForeignKey('TabletMainCamera', on_delete=models.CASCADE, null=True, blank=True)
    tablet_front_camera = models.ForeignKey('TabletFrontCamera', on_delete=models.CASCADE, null=True, blank=True)
    '''--------------------------------------------------------------------------------------------------------------'''
    phone_brand = models.ForeignKey('PhoneBrand', on_delete=models.CASCADE, null=True, blank=True)
    phone_ram = models.ForeignKey('PhoneRAM', on_delete=models.CASCADE, null=True, blank=True)
    phone_built_in_memory = models.ForeignKey('PhoneBuiltInMemory', on_delete=models.CASCADE, null=True, blank=True)
    phone_memory_capacity = models.ForeignKey('PhoneMemoryCapacity', on_delete=models.CASCADE, null=True, blank=True)
    phone_tireless_technologies = models.ForeignKey('PhoneWirelessTechnologies', on_delete=models.CASCADE, null=True, blank=True)
    phone_main_camera_mp = models.ForeignKey('PhoneMainCameraMP', on_delete=models.CASCADE, null=True, blank=True)
    phone_main_camera_features = models.ManyToManyField('PhoneMainCameraFeatures', blank=True)
    phone_front_camera_mp = models.ForeignKey('PhoneFrontCameraMP', on_delete=models.CASCADE, null=True, blank=True)
    phone_processor_name = models.ForeignKey('PhoneProcessorName', on_delete=models.CASCADE, null=True, blank=True)
    phone_display_resolution = models.ForeignKey('PhoneDisplayResolution', on_delete=models.CASCADE, null=True, blank=True)
    phone_matrix_type = models.ForeignKey('PhoneMatrixType', on_delete=models.CASCADE, null=True, blank=True)
    phone_screen_refresh_rate = models.ForeignKey('PhoneScreenRefreshRate', on_delete=models.CASCADE, null=True, blank=True)
    phone_operating_system = models.ForeignKey('PhoneOperatingSystem', on_delete=models.CASCADE, null=True, blank=True)
    phone_equipment = models.ManyToManyField('PhoneEquipment', blank=True)

    class Meta:
        verbose_name = 'Products'
        verbose_name_plural = 'Products'
        managed = True
        ordering = ('-post_date', )

    def __str__(self):
        return self.name


class ProductCategory(models.Model):
    slug = models.SlugField(max_length=30, db_index=True, unique=True)
    name = models.CharField(max_length=30, db_index=True)

    class Meta:
        verbose_name = 'ProductCategory'
        verbose_name_plural = 'ProductCategories'

    def __str__(self):
        return self.name


class LaptopBrand(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class LaptopProcessor(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class LaptopRAM(models.Model):
    name = models.PositiveIntegerField()

    def __str__(self):
        return str(self.name)


class LaptopDescreteGraficsCard(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class LaptopOperatingSystem(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class LaptopSSDCapacity(models.Model):
    name = models.PositiveIntegerField()

    def __str__(self):
        return str(self.name)


class MadeIn(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class LaptopViedoCardMemoryCapacity(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class LaptopScreenType(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class LaptopProcessorCores(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class LaptopVideoCardType(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class LaptopDriveType(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class LaptopRAMType(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class LaptopResolution(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class LaptopBatteryCapacity(models.Model):
    name = models.PositiveIntegerField()

    def __str__(self):
        return str(self.name)


class LaptopScreenRefreshRate(models.Model):
    name = models.PositiveIntegerField()

    def __str__(self):
        return str(self.name)


class ManufactureYear(models.Model):
    name = models.PositiveIntegerField()

    def __str__(self):
        return str(self.name)


class Color(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


'''========================================'''


class TabletBrand(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class TabletRAM(models.Model):
    name = models.PositiveIntegerField()

    def __str__(self):
        return str(self.name)


class TabletBuiltInMemory(models.Model):
    name = models.PositiveIntegerField()

    def __str__(self):
        return str(self.name)


class TabletWirelessCapabilities(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class TabletOperatingSystem(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class TabletMatrixType(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class TabletFeatures(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class TabletScreenResolution(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class TabletProcessorCores(models.Model):
    name = models.PositiveIntegerField()

    def __str__(self):
        return str(self.name)


class TabletProcessor(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class TabletMainCamera(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class TabletFrontCamera(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


'''========================================'''


class PhoneBrand(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class PhoneRAM(models.Model):
    name = models.PositiveIntegerField()

    def __str__(self):
        return str(self.name)


class PhoneBuiltInMemory(models.Model):
    name = models.PositiveIntegerField()

    def __str__(self):
        return str(self.name)


class PhoneMemoryCapacity(models.Model):
    name = models.PositiveIntegerField()

    def __str__(self):
        return str(self.name)


class PhoneWirelessTechnologies(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class PhoneMainCameraMP(models.Model):
    name = models.PositiveIntegerField()

    def __str__(self):
        return str(self.name)


class PhoneMainCameraFeatures(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class PhoneFrontCameraMP(models.Model):
    name = models.PositiveIntegerField()

    def __str__(self):
        return str(self.name)


class PhoneProcessorName(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class PhoneDisplayResolution(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class PhoneMatrixType(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class PhoneScreenRefreshRate(models.Model):
    name = models.PositiveIntegerField()

    def __str__(self):
        return str(self.name)


class PhoneOperatingSystem(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class PhoneEquipment(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


'''========================================'''


class NumberOfSIMCards(models.Model):
    name = models.PositiveIntegerField()

    def __str__(self):
        return str(self.name)

