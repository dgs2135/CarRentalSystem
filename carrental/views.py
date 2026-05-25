from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import VehicleBrand, Vehicle, Booking, Testimonial, ContactQuery, Subscriber, PageContent
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .models import Booking
from django.contrib.admin.views.decorators import staff_member_required
import json
from django.utils import timezone

def home(request):
    vehicles = Vehicle.objects.filter(available=True)
    brands = VehicleBrand.objects.filter(vehicle__available=True).distinct().order_by('name')
    descriptions = vehicles.values_list('description', flat=True).distinct().order_by('description')
    return render(request, 'carrental/home.html', {'vehicles': vehicles, 'brands': brands, 'descriptions': descriptions})

def contact(request):
    if request.method == 'POST':
        ContactQuery.objects.create(
            name=request.POST['name'],
            email=request.POST['email'],
            message=request.POST['message']
        )
        messages.success(request, 'Query submitted successfully!')
        return redirect('contact')
    content = PageContent.objects.filter(page_name='contact').first()
    return render(request, 'carrental/contact.html', {'content': content.content if content else ''})

@login_required
def car_booking(request):
    if request.method == 'POST':
        vehicle_ids = request.POST.getlist('vehicle_id[]')
        start_dates = request.POST.getlist('start_date[]')
        end_dates = request.POST.getlist('end_date[]')

        if not (len(vehicle_ids) == len(start_dates) == len(end_dates)):
            messages.error(request, 'Invalid booking data submitted.')
            return redirect('car_booking')

        for vehicle_id, start_date, end_date in zip(vehicle_ids, start_dates, end_dates):
            vehicle = Vehicle.objects.get(id=vehicle_id)
            Booking.objects.create(user=request.user, vehicle=vehicle, start_date=start_date, end_date=end_date)
            vehicle.available = False
            vehicle.save()

        messages.success(request, 'Car(s) booked successfully!')
        return redirect('booking_history')

    vehicles = Vehicle.objects.filter(available=True)
    brands = VehicleBrand.objects.all()
    if not vehicles.exists():
        messages.info(request, 'No vehicles are currently available for booking.')
    return render(request, 'carrental/car_booking.html', {
        'vehicles': vehicles,
        'brands': brands
    })

@login_required
def booking_history(request):
    # Delete expired bookings
    current_date = timezone.now().date()
    Booking.objects.filter(end_date__lt=current_date).delete()
    
    # Get remaining bookings
    bookings = Booking.objects.filter(user=request.user).order_by('-start_date')
    return render(request, 'carrental/booking_history.html', {'bookings': bookings})

@login_required
def testimonials(request):
    testimonials = Testimonial.objects.filter(is_active=True).select_related('user__profile')
    if not testimonials.exists():
        messages.info(request, 'No active testimonials available yet.')
    return render(request, 'carrental/testimonials.html', {'testimonials': testimonials})

@login_required
def post_testimonial(request):
    if request.method == 'POST':
        content = request.POST.get('content')
        image = request.FILES.get('image')
        
        testimonial = Testimonial(
            user=request.user,
            content=content,
            image=image
        )
        testimonial.save()
        
        return redirect('testimonials')
        
    return render(request, 'carrental/post_testimonial.html')

@login_required
def dashboard(request):
    stats = {
        'users': User.objects.count(),
        'bookings': Booking.objects.count(),
        'subscribers': Subscriber.objects.count(),
        'queries': ContactQuery.objects.count(),
    }
    bookings = Booking.objects.select_related('user', 'vehicle').all()
    return render(request, 'carrental/dashboard.html', {'stats': stats, 'bookings': bookings})

@staff_member_required
def admin_change_booking(request, pk):
    return redirect(f'/admin/carrental/booking/{pk}/change/')
