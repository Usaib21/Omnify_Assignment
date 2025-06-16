from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import FitnessClass, Booking
from .serializers import FitnessClassSerializer, BookingSerializer, BookingRequestSerializer
from django.utils.timezone import localtime

@api_view(['GET'])
def get_classes(request):
    classes = FitnessClass.objects.all().order_by('datetime')
    serializer = FitnessClassSerializer(classes, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def book_class(request):
    serializer = BookingRequestSerializer(data=request.data)
    if serializer.is_valid():
        try:
            fitness_class = FitnessClass.objects.get(id=serializer.validated_data['class_id'])
            if fitness_class.available_slots <= 0:
                return Response({"error": "No slots available."}, status=status.HTTP_400_BAD_REQUEST)
            booking = Booking.objects.create(
                fitness_class=fitness_class,
                client_name=serializer.validated_data['client_name'],
                client_email=serializer.validated_data['client_email']
            )
            # fitness_class.available_slots -= 1
            # fitness_class.save()
            return Response(BookingSerializer(booking).data, status=status.HTTP_201_CREATED)
        except FitnessClass.DoesNotExist:
            return Response({"error": "Class not found."}, status=status.HTTP_404_NOT_FOUND)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_bookings(request):
    email = request.GET.get('email')
    if not email:
        return Response({"error": "Email parameter is required."}, status=status.HTTP_400_BAD_REQUEST)
    bookings = Booking.objects.filter(client_email=email)
    serializer = BookingSerializer(bookings, many=True)
    return Response(serializer.data)
