from django.db.models import Q
from rest_framework import serializers

from chat.models import ChatRoom, Message
from chat.serializers import ChatRoomSerializer, MessagesSerializer
from products.models import Products, ProductCategory, Rating, Attachments
from reviews.serializers import ReviewsListSerializer


class AttachmentsSerializer(serializers.ModelSerializer):
    photo = serializers.ImageField()

    class Meta:
        model = Attachments
        fields = ['photo']


class AttachmentsCreateSerializer(serializers.Serializer):
    product = serializers.SlugRelatedField(slug_field='name', read_only=True)
    photos = serializers.ListField(child=serializers.ImageField())

    def create(self, validated_data):
        photos = validated_data.get('photos')
        product = validated_data.get('product')
        attach = []
        for photo in photos:
            attach.append(Attachments.objects.create(photo=photo, product=product))
        print('========================', attach)
        return {'product': product, 'photos': [instance.photo for instance in attach]}


class RatingCreateSerializer(serializers.ModelSerializer):
    product = serializers.SlugRelatedField(slug_field='name', read_only=True)
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Rating
        fields = '__all__'

    def create(self, validated_data):
        rating, created = Rating.objects.update_or_create(
            owner=validated_data.get('owner'),
            product=validated_data.get('product'),
            defaults={'rate': validated_data.get('rate')}
        )
        return rating


class RatingSerializer(serializers.ModelSerializer):
    product = serializers.SlugRelatedField(slug_field='name', read_only=True)
    owner = serializers.SlugRelatedField(slug_field='display_name', read_only=True)

    class Meta:
        model = Rating
        fields = '__all__'


class ProductsListSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(slug_field='name', read_only=True)
    owner = serializers.SlugRelatedField(slug_field='display_name', read_only=True)
    reviews = ReviewsListSerializer(many=True)
    attachments = AttachmentsSerializer(many=True)
    chat = serializers.SerializerMethodField()
    rated_by = serializers.SerializerMethodField()
    made_in = serializers.SlugRelatedField(slug_field='name', read_only=True)

    class Meta:
        model = Products
        fields = ('id', 'slug', 'name', 'owner', 'category', 'made_in', 'photo', 'price', 'discount', 'rate', 'rated_by', 'sold', 'description', 'post_date', 'chat', 'attachments', 'reviews')
        lookup_field = 'slug'

    def get_chat(self, obj):
        item = Products.objects.get(slug=obj.slug)
        if self.context['request'].user != obj.owner:
            try:
                chat = ChatRoom.objects.filter(members__in=[obj.owner, self.context['request'].user], product__slug=obj.slug).distinct().get()
                print(chat.created_at, '--------------------------------------------')
                chat_json = ChatRoomSerializer(chat).data
                messages = Message.objects.filter(chat_room=chat)
                messages_json = MessagesSerializer(messages, many=True).data
                chat_json['messages'] = messages_json
                return chat_json
            except ChatRoom.DoesNotExist:
                return 'Chat Available'

        return 'Chat is not available'

    def get_rated_by(self, obj):
        user = self.context['request'].user
        try:
            rate = Rating.objects.get(product__slug=obj.slug, owner=user)
            return RatingSerializer(rate).data['rate']
        except Rating.DoesNotExist:
            return None


class LaptopCreateSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
    category = serializers.HiddenField(default=ProductCategory.objects.get(name='Laptop'))

    class Meta:
        model = Products
        fields = (
            'owner',
            'name',
            'category',
            'made_in',
            'photo',
            'video',
            'price',
            'discount',
            'screen_diagonal',
            'weight',
            'manufacture_year',
            'color',
            'amount',
            'description',
            'laptop_brand',
            'laptop_processor',
            'laptop_ram',
            'laptop_descrete_grafics_card',
            'laptop_operating_system',
            'laptop_sssd_capacity',
            'laptop_video_card_memory_capacity',
            'laptop_screentype',
            'laptop_processor_cores',
            'laptop_videocard_type',
            'laptop_drive_type',
            'laptop_ram_type',
            'laptop_resolution',
            'laptop_battery_capacity',
            'laptop_screen_refresh_rate',
        )


class PhoneCreateSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
    category = serializers.HiddenField(default=ProductCategory.objects.get(name='Phone'))

    class Meta:
        model = Products
        fields = (
            'owner',
            'name',
            'category',
            'made_in',
            'photo',
            'video',
            'price',
            'discount',
            'screen_diagonal',
            'weight',
            'manufacture_year',
            'color',
            'amount',
            'description',
            'number_of_sim_cards',
            'phone_brand',
            'phone_ram',
            'phone_built_in_memory',
            'phone_memory_capacity',
            'phone_tireless_technologies',
            'phone_main_camera_mp',
            'phone_main_camera_features',
            'phone_front_camera_mp',
            'phone_processor_name',
            'phone_display_resolution',
            'phone_matrix_type',
            'phone_screen_refresh_rate',
            'phone_operating_system',
            'phone_equipment',
        )


class TabletCreateSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
    category = serializers.HiddenField(default=ProductCategory.objects.get(name='Tablet'))

    class Meta:
        model = Products
        fields = (
            'owner',
            'name',
            'category',
            'made_in',
            'photo',
            'video',
            'price',
            'discount',
            'screen_diagonal',
            'weight',
            'manufacture_year',
            'color',
            'amount',
            'description',
            'number_of_sim_cards',
            'tablet_brand',
            'tablet_ram',
            'tablet_built_in_memory',
            'tablet_wireless_capabilities',
            'tablet_operating_system',
            'tablet_matrix_type',
            'tablet_features',
            'tablet_screen_resolution',
            'tablet_processor_cores',
            'tablet_processor',
            'tablet_main_camera',
            'tablet_front_camera',
        )


class LaptopUpdateSerializer(serializers.ModelSerializer):
    slug = serializers.ReadOnlyField()
    rate = serializers.ReadOnlyField()

    class Meta:
        model = Products
        fields = (
            'id',
            'slug',
            'post_date',
            'name',
            'category',
            'rate',
            'made_in',
            'photo',
            'video',
            'price',
            'discount',
            'screen_diagonal',
            'weight',
            'manufacture_year',
            'color',
            'amount',
            'description',
            'laptop_brand',
            'laptop_processor',
            'laptop_ram',
            'laptop_descrete_grafics_card',
            'laptop_operating_system',
            'laptop_sssd_capacity',
            'laptop_video_card_memory_capacity',
            'laptop_screentype',
            'laptop_processor_cores',
            'laptop_videocard_type',
            'laptop_drive_type',
            'laptop_ram_type',
            'laptop_resolution',
            'laptop_battery_capacity',
            'laptop_screen_refresh_rate',
        )


class PhoneUpdateSerializer(serializers.ModelSerializer):
    slug = serializers.ReadOnlyField()
    rate = serializers.ReadOnlyField()

    class Meta:
        model = Products
        fields = (
            'id',
            'slug',
            'post_date',
            'name',
            'category',
            'rate',
            'made_in',
            'photo',
            'video',
            'price',
            'discount',
            'screen_diagonal',
            'weight',
            'manufacture_year',
            'color',
            'amount',
            'description',
            'number_of_sim_cards',
            'phone_brand',
            'phone_ram',
            'phone_built_in_memory',
            'phone_memory_capacity',
            'phone_tireless_technologies',
            'phone_main_camera_mp',
            'phone_main_camera_features',
            'phone_front_camera_mp',
            'phone_processor_name',
            'phone_display_resolution',
            'phone_matrix_type',
            'phone_screen_refresh_rate',
            'phone_operating_system',
            'phone_equipment',
        )


class TabletUpdateSerializer(serializers.ModelSerializer):
    slug = serializers.ReadOnlyField()
    rate = serializers.ReadOnlyField()

    class Meta:
        model = Products
        fields = (
            'id',
            'slug',
            'post_date',
            'name',
            'category',
            'rate',
            'made_in',
            'photo',
            'video',
            'price',
            'discount',
            'screen_diagonal',
            'weight',
            'manufacture_year',
            'color',
            'amount',
            'description',
            'number_of_sim_cards',
            'tablet_brand',
            'tablet_ram',
            'tablet_built_in_memory',
            'tablet_wireless_capabilities',
            'tablet_operating_system',
            'tablet_matrix_type',
            'tablet_features',
            'tablet_screen_resolution',
            'tablet_processor_cores',
            'tablet_processor',
            'tablet_main_camera',
            'tablet_front_camera',
        )


class LaptopDetailSerializer(LaptopUpdateSerializer):
    category = serializers.SlugRelatedField(slug_field='name', read_only=True)
    owner = serializers.SlugRelatedField(slug_field='display_name', read_only=True)
    color = serializers.SlugRelatedField(slug_field='name', read_only=True)
    manufacture_year = serializers.SlugRelatedField(slug_field='name', read_only=True)
    made_in = serializers.SlugRelatedField(slug_field='name', read_only=True)

    class Meta:
        model = Products
        fields = (('id', 'slug', 'post_date', 'owner', 'sold', 'category', 'rate') + LaptopUpdateSerializer.Meta.fields)


class PhoneDetailSerializer(PhoneUpdateSerializer):
    category = serializers.SlugRelatedField(slug_field='name', read_only=True)
    owner = serializers.SlugRelatedField(slug_field='display_name', read_only=True)
    color = serializers.SlugRelatedField(slug_field='name', read_only=True)
    manufacture_year = serializers.SlugRelatedField(slug_field='name', read_only=True)
    made_in = serializers.SlugRelatedField(slug_field='name', read_only=True)

    class Meta:
        model = Products
        fields = ('id', 'slug', 'post_date', 'owner', 'sold', 'category', 'rate')


class TabletDetailSerializer(TabletUpdateSerializer):
    category = serializers.SlugRelatedField(slug_field='name', read_only=True)
    owner = serializers.SlugRelatedField(slug_field='display_name', read_only=True)
    color = serializers.SlugRelatedField(slug_field='name', read_only=True)
    manufacture_year = serializers.SlugRelatedField(slug_field='name', read_only=True)
    made_in = serializers.SlugRelatedField(slug_field='name', read_only=True)

    class Meta:
        model = Products
        fields = ('id', 'slug', 'owner', 'post_date', 'sold', 'category', 'rate') + TabletUpdateSerializer.Meta.fields

