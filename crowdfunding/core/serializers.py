from rest_framework import serializers
from django.contrib.auth.models import User

from .models import Collect, Payment


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class PaymentSerializer(serializers.ModelSerializer):
    collect = serializers.StringRelatedField()
    user = UserSerializer(read_only=True)

    class Meta:
        model = Payment
        fields = ['id', 'collect', 'user', 'amount', 'created_at']


class CollectSerializer(serializers.ModelSerializer):
    payments = PaymentSerializer(many=True, read_only=True)
    author = UserSerializer(read_only=True)
    cover_image = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = Collect
        fields = [
            'id', 'author', 'title', 'occasion', 'description',
            'target_amount', 'collected_amount', 'donors_count',
            'cover_image', 'end_date', 'payments'
        ]
        read_only_fields = ['author', 'collected_amount', 'donors_count']
