from rest_framework import serializers

from manufacture.models import Manufacture


class ManufactureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manufacture
        fields = ("id", "name", "country", "car_type", "created_at")