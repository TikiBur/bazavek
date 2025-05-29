from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Booking(models.Model):
    house_id = models.CharField(max_length=20)
    house_title = models.CharField(max_length=100)
    house_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    guests = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )

    start_date = models.DateField()
    end_date = models.DateField()
    nights = models.PositiveIntegerField(editable=False)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, editable=False)

    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    _date_range = None

    def save(self, *args, **kwargs):
        if self.start_date and self.end_date:
            self.nights = (self.end_date - self.start_date).days
            self.total_price = self.nights * self.house_price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.house_title} ({self.start_date} - {self.end_date})"

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Бронирование'
        verbose_name_plural = 'Бронирования'

class Testimonial(models.Model):
    name = models.CharField(max_length=100)
    rating = models.PositiveSmallIntegerField()
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name} - {self.rating}'