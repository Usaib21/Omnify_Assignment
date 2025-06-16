from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone

class FitnessClass(models.Model):
    CLASS_TYPES = [
        ('YOGA', 'Yoga'),
        ('ZUMBA', 'Zumba'),
        ('HIIT', 'HIIT'),
    ]
    
    name = models.CharField(max_length=50, choices=CLASS_TYPES)
    datetime = models.DateTimeField()
    instructor = models.CharField(max_length=100)
    total_slots = models.PositiveIntegerField()
    available_slots = models.PositiveIntegerField(blank=True, null=True,
                                                 help_text="Leave blank to default to total_slots")
        
    def clean(self):
        if self.total_slots is not None and self.available_slots is not None:
            if self.available_slots > self.total_slots:
                raise ValidationError({
                    "available_slots": "Available slots cannot exceed total slots."
                })
            if self.available_slots < 0:
               raise ValidationError({
                    "available_slots": "Available slots cannot be negative."
                })


    def save(self, *args, **kwargs):
        if self._state.adding and self.available_slots is None:
            self.available_slots = self.total_slots
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        local_dt = timezone.localtime(self.datetime).strftime('%Y-%m-%d %H:%M')
        return f"{self.get_name_display()} with {self.instructor} at {local_dt}"

class Booking(models.Model):
    fitness_class = models.ForeignKey(
        FitnessClass,
        on_delete=models.CASCADE,
        related_name='bookings'
    )
    client_name = models.CharField(max_length=100)
    client_email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.fitness_class.available_slots <= 0:
            raise ValidationError("No slots available for this class.")

    def save(self, *args, **kwargs):
        self.full_clean()
        self.fitness_class.available_slots -= 1
        self.fitness_class.save(update_fields=['available_slots'])
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.client_name} → {self.fitness_class}"
