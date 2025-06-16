from rest_framework import serializers
from .models import FitnessClass, Booking
from django.utils.timezone import localtime

class FitnessClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = FitnessClass
        fields = ['id', 'name', 'datetime', 'instructor', 'available_slots']

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'

class BookingRequestSerializer(serializers.Serializer):
    class_id = serializers.IntegerField()
    client_name = serializers.CharField(max_length=100)
    client_email = serializers.EmailField()
