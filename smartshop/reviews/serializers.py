from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from reviews.models import Reviews, Like


class ReviewsListSerializer(serializers.ModelSerializer):
    owner = serializers.SlugRelatedField(slug_field='display_name', read_only=True)
    product = serializers.SlugRelatedField(slug_field='name', read_only=True)
    referred_by = serializers.SlugRelatedField(slug_field='id', read_only=True, many=True)
    liked_by_user = serializers.SerializerMethodField()

    class Meta:
        model = Reviews
        fields = '__all__'

    def get_liked_by_user(self, obj):
        review = Like.objects.filter(liked=True, owner=self.context['request'].user, review__id=obj.id)
        if review:
            return True
        else:
            return False


class ReviewsCreateSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
    product = serializers.SlugRelatedField(slug_field='name', read_only=True)
    refers_to = serializers.SlugRelatedField(slug_field='id', read_only=True)
    likes = serializers.ReadOnlyField()

    class Meta:
        model = Reviews
        fields = '__all__'


class ReviewsUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Reviews
        fields = ['text']


class LikeReviewSerializer(serializers.ModelSerializer):
    owner = serializers.SlugRelatedField(slug_field='display_name', read_only=True)
    product = serializers.SlugRelatedField(slug_field='name', read_only=True)
    refers_to = serializers.SlugRelatedField(slug_field='id', read_only=True)
    likes = serializers.ReadOnlyField()

    class Meta:
        model = Reviews
        exclude = ['text']

