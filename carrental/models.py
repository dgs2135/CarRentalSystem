from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

class VehicleBrand(models.Model):
    name = models.CharField(max_length=100, unique=True)
    def __str__(self):
        return self.name

class Vehicle(models.Model):
    brand = models.ForeignKey(VehicleBrand, on_delete=models.CASCADE)
    model = models.CharField(max_length=100)
    description = models.TextField()
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    def __str__(self):
        return f"{self.brand} {self.model}"

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=(('Pending', 'Pending'), ('Confirmed', 'Confirmed'), ('Cancelled', 'Cancelled')), default='Pending')
    def __str__(self):
        return f"{self.user.username} - {self.vehicle}"

class Testimonial(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='testimonials/', null=True, blank=True)
    def __str__(self):
        return f"{self.user.username} - {self.created_at}"

class ContactQuery(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name

class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    def __str__(self):
        return self.email

class PageContent(models.Model):
    page_name = models.CharField(max_length=50, unique=True)
    content = models.TextField()
    def __str__(self):
        return self.page_name
    
@receiver(post_delete, sender=Booking)
@receiver(post_save, sender=Booking)
def update_vehicle_availability(sender, instance, **kwargs):
    """
    Update vehicle availability when bookings are created/deleted
    """
    vehicle = instance.vehicle
    # Check if vehicle has any active bookings
    has_active_bookings = Booking.objects.filter(
        vehicle=vehicle,
        status__in=['Pending', 'Confirmed']
    ).exists()
    # Update availability
    vehicle.available = not has_active_bookings
    vehicle.save()