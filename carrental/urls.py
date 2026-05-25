from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('booking/', views.car_booking, name='car_booking'),
    path('history/', views.booking_history, name='booking_history'),
    path('testimonials/', views.testimonials, name='testimonials'),
    path('post-testimonial/', views.post_testimonial, name='post_testimonial'),
    path('contact/', views.contact, name='contact'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('admin/booking/<int:pk>/change/', views.admin_change_booking, name='admin_change_booking'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
