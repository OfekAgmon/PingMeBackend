__author__ = 'ofeka_000'
from rest_framework import serializers
from django.contrib.auth.models import User
from pingme.models import Device, Location


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email', )
        extra_kwargs = {'password': {'write_only': True}}

    def init(self, *args, **kwargs):
        super(UserSerializer, self).__init__(*args, **kwargs)
        self.fields['username'].validators = []

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data['email'],
        )

        user.set_password(validated_data['password'])
        user.save()
        return user

class DeviceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Device
        fields = ('device_id', )
        read_only_fields = ('user', )


class LocationSerializer(serializers.ModelSerializer):

    user = UserSerializer(many=False, required=False)

    class Meta:
        model = Location
        fields = ('latitude', 'longitude', 'id', 'user', )
        read_only_fields = ('user', )