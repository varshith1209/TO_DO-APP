from rest_framework import serializers
from .models import tasks


class taskserializer(serializers.ModelSerializer):
    class Meta:
        model=tasks
        fields="__all__"
        read_only_fields=['user']
        