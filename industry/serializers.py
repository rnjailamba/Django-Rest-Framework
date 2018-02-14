from .models import Industry
from django.contrib.auth.models import User
from rest_framework import serializers


class IndustrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Industry
        fields = ('industry_id', 'name', 'parent_ids', 'direct_parent_id')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password')