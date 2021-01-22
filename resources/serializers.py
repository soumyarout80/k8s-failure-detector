from rest_framework import serializers
from .models import Resource
from .models import Alert
from .models import Account
from .models import User


class ResourceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = '__all__'


class AlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alert
        fields = '__all__'


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'
