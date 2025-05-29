from django.contrib import admin
from .models import Booking

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'house_title', 'start_date', 'end_date', 'guests', 'total_price', 'name', 'created_at')
    list_filter = ('house_id', 'start_date', 'created_at')
    search_fields = ('name', 'email', 'phone', 'house_title')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)