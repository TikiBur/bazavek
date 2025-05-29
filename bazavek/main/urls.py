from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.index, name='index'),
    path('rentals/', views.rentals_view, name='rentals'),
    path('book/', views.book_house, name='book_house'),
    path('testimonials/', views.testimonials_list, name='testimonials'),
    path('testimonial-create/', views.testimonial_create, name='testimonial_create'),
    path('support/', views.support, name='support'),
    path('booking-success/', views.booking_success, name='booking_success'),
]