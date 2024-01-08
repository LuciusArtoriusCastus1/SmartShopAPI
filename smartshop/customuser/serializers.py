from rest_framework import serializers
from djoser.serializers import UserCreateSerializer, UserSerializer
from customuser.models import User


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = '__all__'


class UserRegistrationSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        fields = ('email', 'display_name', 'first_name', 'last_name', 'profile_image', 'password', 'bio', 'gender')


class UserUpdateSerializer(UserSerializer):
    class Meta(UserCreateSerializer.Meta):
        fields = ('email', 'display_name', 'first_name', 'last_name', 'profile_image', 'password', 'bio', 'gender')

    def get_fields(self):
        fields = super().get_fields()
        if self.context['request'].user.paypal_email is not None:
            fields['paypal_email'] = serializers.CharField()
            return fields
        else:
            return fields


class SellerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('paypal_email', )

