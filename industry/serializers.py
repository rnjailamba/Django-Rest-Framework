from .models import Industry
from rest_framework import serializers


class IndustrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Industry
        fields = ('industry_id', 'name')