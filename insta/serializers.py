from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from insta.models import Insta

class InstaUserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Insta
        fields = '__all__'

    def save(self, validated_data):
        insta = Insta.objects.create(
            name=validated_data['name'],
            IP=validated_data['IP'],
            password=make_password(validated_data['password']),
        )
        return insta