from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APIClient
from rest_framework import status
from .models import FitnessClass

class BookingAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.class1 = FitnessClass.objects.create(
            name='YOGA',
            datetime=timezone.now() + timezone.timedelta(days=1),
            instructor='John Doe',
            total_slots=10,
            available_slots=10
        )

    def test_get_classes(self):
        response = self.client.get('/api/classes')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_booking(self):
        data = {
            'class_id': self.class1.id,
            'client_name': 'Alice',
            'client_email': 'alice@example.com'
        }
        response = self.client.post('/api/book', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.class1.refresh_from_db()
        self.assertEqual(self.class1.available_slots, 9)

    def test_overbooking(self):
        self.class1.available_slots = 0
        self.class1.save()

        data = {
            'class_id': self.class1.id,
            'client_name': 'Bob',
            'client_email': 'bob@example.com'
        }
        response = self.client.post('/api/book', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_bookings(self):
        # Create booking
        data = {
            'class_id': self.class1.id,
            'client_name': 'Charlie',
            'client_email': 'charlie@example.com'
        }
        self.client.post('/api/book', data, format='json')

        # Get bookings
        response = self.client.get('/api/bookings?email=charlie@example.com')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
